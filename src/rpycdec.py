"""
Module decompile rpyc files. 
"""


import argparse
import io
import logging
import os
import pickle
import pickletools
import re
import sqlite3
import struct
import time
import zipfile
import zlib
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from typing import Callable

import requests
from ratelimit import limits, sleep_and_retry

import renpy.ast
import renpy.sl2.slast
import renpy.util

# A string at the start of each rpycv2 file.
RPYC2_HEADER = b"RENPY RPC2"

logger = logging.getLogger(__name__)


class GoogleTranslator:
    """
    Google translate api wrapper
    """

    session = requests.Session()

    def __init__(self, src: str = "auto", dest: str = "zh-CN") -> None:
        self.src_lang = src
        self.dest_lang = dest

    @sleep_and_retry
    # limit calls per second
    @limits(calls=5, period=1)
    # google translate api is not free, so use cache
    def translate(self, text: str) -> str:
        """
        Translate text to dest language
        """
        if text.strip() == "" or re.match(r"^[0-9\W]+$", text):
            return text
        forms = {
            "client": "gtx",
            "sl": self.src_lang,
            "tl": self.dest_lang,
            "dt": "t",
            "q": text,
        }
        server = "https://translate.google.com"
        resp = self.session.post(f"{server}/translate_a/single", data=forms)
        if resp.status_code != 200:
            raise ValueError(f"translate error: {resp.status_code}")
        data = resp.json()
        segments = ""
        for sec in data[0]:
            segments += sec[0]
        return segments


class CachedTranslator:
    """
    Translator wrapper with cache.
    Use local disk cache to avoid translate same text again and again.
    """

    cache = {}
    _translate: Callable[[str], str]

    def __init__(self, translator: Callable[[str], str], cache_dir=".cache") -> None:
        self._translate = translator
        # make sure cache dir exists
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        conn = sqlite3.connect(cache_dir + "/cache.sqlite")
        # create table if not exists
        conn.cursor().execute(
            "create table if not exists cache (key text primary key, value text)"
        )
        self.cache = conn

    def get(self, key: str) -> str:
        result = (
            self.cache.cursor()
            .execute("select (value) from cache where key = ?", (key,))
            .fetchone()
        )
        return result[0] if result else None

    def put(self, key: str, val: str):
        self.cache.cursor().execute(
            "insert into cache (key, value) values (?, ?)", (key, val)
        )
        self.cache.commit()

    def translate(self, text: str) -> str:
        """
        translate text and cache it
        """
        start_time = time.time()
        logger.debug(">>> [%s]", text)
        cachekey = sha256(text.encode()).hexdigest()
        cached = self.get(cachekey)
        if cached:
            decoded = cached
            logger.debug("<-- [%s]", decoded)
            return decoded
        translated = self._translate(text)
        self.put(cachekey, translated)
        cost_time = time.time() - start_time
        logger.debug("<<< [%s] [cost %f.2s]", translated, cost_time)
        return translated


class CodeTranslator:
    """
    Translate warpped for renpy code.
    Parse text in renpy code(block, expr, text) and translate it.
    """

    _translator: Callable[[str], str]

    def __init__(self, translator: Callable[[str], str]) -> None:
        """
        Parameters
        ----------
        translator : Callable[[str], str]
            translator function
        """
        self.translator = translator

    def _call_translate(self, line) -> str:
        return self.translator(line)

    def trans_placeholder(self, line) -> str:
        """
        1. repalace placeholders with @
        2. translate
        3. replace back @ with placeholders

        To avoid translate chars in placeholders

        eg:

        bad:  {color=#ff0000}hello{/color}  -> {颜色=#ff0000}你好{/颜色}
        good: {color=#ff0000}hello{/color}  -> @你好@ -> {color=#ff0000}你好{/color}
        """
        ph_ch = "@"  # placeholder char
        phs = []
        totranslate = ""
        # {}  []
        braces, squares = [], []
        for i, char in enumerate(line):
            if i > 0 and line[i - 1] == "\\":
                totranslate += char
                continue
            if char =='[':
                squares.append(i)
            elif char ==']':
                end = squares.pop()
                if squares:
                    continue
                phs.append(line[end : i + 1])
                totranslate += ph_ch
            elif char =='{':
                braces.append(i)
            elif char =='}':
                if braces:
                    end = braces.pop()
                    if braces:
                        continue
                    phs.append(line[end : i + 1])
                    totranslate += ph_ch
            else:
                if not squares and not braces:
                        totranslate += char

        translated = self._call_translate(totranslate) if totranslate else line
        for placeholder in phs:
            # translate in placeholder
            # e.g. "{#r=hello}"
            matched = re.search(r"{#\w=(.+?)}", placeholder)
            if matched:
                translated = self.trans_placeholder(matched.group(1))
                placeholder = (
                    placeholder[: matched.start(1)]
                    + translated
                    + placeholder[matched.end(1) :]
                )
            translated = translated.replace(ph_ch, placeholder, 1)
        return translated

    def _on_text(self, text: str) -> str:
        if text.strip() == "":
            return text
        if text[0] == '"' and text[-1] == '"':
            return '"' + self._on_text(text[1:-1]) + '"'
        if "%" in text:  # format string
            return text
        result = self.trans_placeholder(text)
        result = result.replace("%", "")
        return result

    def _on_expr(self, expr: str) -> str:
        prev_end, dquoters = 0, []
        result = ""
        for i, char in enumerate(expr):
            if i > 0 and expr[i - 1] == "\\":
                continue
            if char == '"':
                if not dquoters:
                    result += expr[prev_end:i]
                    dquoters.append(i)
                else:
                    result += self._on_text(expr[dquoters.pop() : i + 1])
                    prev_end = i + 1
        result += expr[prev_end:]
        return result

    def _on_block(self, code: str) -> str:
        """
        find strings in python expr and translate it
        """
        results = []
        for text in code.splitlines():
            result = ""
            prev_end = 0
            # match _("hello") 's hello
            for find in re.finditer(r'_\("(.+?)"\)', text):
                start, group, end = find.start(1), find.group(1), find.end(1)
                result += text[prev_end:start] + self._on_text(group)
                prev_end = end
            result += text[prev_end:]
            results.append(result)
        return "\n".join(results)

    def translate(self, kind, text) -> str:
        """
        translate text by kind

        Parameters
        ----------
        kind : str
            text, expr, block
        text : str
            text to translate
        """
        if kind =='text':
            text = self._on_text(text)
        elif kind =='expr':
            text = self._on_expr(text)
        elif kind =='block':
             text = self._on_block(text)
        else:
            text = self._on_text(text)
        return text


def noop_translator(text: str) -> str:
    """
    translate that do nothing but return text self
    """
    return text


def walk_node(node, callback, **kwargs):
    """
    callback: (kind, label, lang, old, new) -> translated

    walk ast node and call callback on nodes that contains text/expr/block
    """
    p_label, p_lang = kwargs.get("label"), kwargs.get("language")
    if isinstance(node, renpy.ast.Translate):
        pass
    elif isinstance(node, renpy.ast.TranslateString):
        node.new = callback(("text", p_label, node.language, node.old, node.new))
    elif isinstance(node, renpy.ast.TranslateBlock):
        pass
    elif isinstance(node, renpy.ast.Say):
        node.what = callback(("text", p_label, p_lang, node.what, None))
    elif isinstance(node, renpy.sl2.slast.SLDisplayable):
        if node.get_name() in ["text", "textbutton"]:
            for i, val in enumerate(node.positional):
                node.positional[i] = callback(("expr", p_lang, p_label, val, None))
    elif isinstance(node, renpy.ast.Show):
        pass
    elif isinstance(node, renpy.ast.UserStatement):
        pass
    elif isinstance(node, renpy.ast.PyCode):
        state = list(node.state)
        state[1] = callback(("block", p_label, p_lang, state[1], None))
        node.state = tuple(state)
    elif isinstance(node, renpy.sl2.slast.SLBlock):
        pass
    elif isinstance(node, renpy.sl2.slast.SLUse):
        if node.args:
            for i, (name, val) in enumerate(node.args.arguments):
                val = callback(("block", p_label, p_lang, val, None))
                node.args.arguments[i] = (name, val)
    elif isinstance(node, renpy.ast.Menu):
        for i, item in enumerate(node.items):
            _li = list(item)
            _li[0] = callback(("text", p_label, p_lang, _li[0], None))
            node.items[i] = tuple(_li)


def _do_consume(meta: tuple, cache: dict) -> str:
    (_, label, _, old, new) = meta
    key, val = label or old, new or old
    return cache.get(key) or val


def _do_collect(meta: tuple, accept_lang: str, into: dict) -> str:
    (kind, label, lang, old, new) = meta
    key, val = label or old, new or old
    if accept_lang and lang and lang != accept_lang:
        return val
    if lang or (not lang and key not in into):
        into[key] = (kind, val)
    return val


def _walk_callback(stmts, callback) -> str:
    return renpy.util.get_code(
        stmts,
        modifier=lambda node, **kwargs: walk_node(node, callback, **kwargs),
    )


def default_translator() -> Callable[[str], str]:
    """
    default translator which use google translate api with CachedTranslator
    """
    return CachedTranslator(GoogleTranslator().translate).translate


def translate_files(
    base_dir: str,
    files,
    translator: Callable[[str], str],
    include_tl_lang: str = "english",
    concurent: int = 0,
):
    """
    translate files and return a map of filename and code
    """
    if not translator:
        logger.info("using default translator")
        translator = default_translator()
    stmts_dict = {}
    translations_dict = {}
    # load translations
    for filename in files:
        logger.info("loading %s", filename)
        stmts = load_file(os.path.join(base_dir, filename))
        stmts_dict[filename] = stmts
        _walk_callback(
            stmts,
            lambda meta: _do_collect(meta, include_tl_lang, translations_dict),
        )
    logger.info("loaded %d translations", len(translations_dict))

    # translate
    logger.info("translating")
    results_dict = {}
    code_translator = CodeTranslator(translator)
    if concurent:
        logger.info("translating with %d concurent", concurent)
        with ThreadPoolExecutor(max_workers=concurent) as executor:
            results = executor.map(
                lambda item: (
                    item[0],
                    code_translator.translate(item[1][0], item[1][1]),
                ),
                translations_dict.items(),
            )
            for label, result in results:
                results_dict[label] = result
                logger.info(
                    "translated %d/%d", len(results_dict), len(translations_dict)
                )
    else:
        for label, (kind, text) in translations_dict.items():
            results_dict[label] = code_translator.translate(kind, text)
            logger.info("translated %d/%d", len(results_dict), len(translations_dict))

    # generate code
    code_files = {}
    logger.info("generating code")
    for filename, stmts in stmts_dict.items():
        logger.info("gnerating code for %s", filename)
        code_files[filename] = _walk_callback(
            stmts, lambda meta: _do_consume(meta, results_dict)
        )
    return code_files


def translate(
    input_path,
    output_path=None,
    translator: Callable[[str], str] = None,
    include_tl_lang: str = "english",
    concurent: int = 0,
):
    """
    translate rpyc file or directory
    """
    if os.path.isfile(input_path):
        if not output_path:
            output_path = input_path.removesuffix("c")
        (_, code) = translate_files(
            "",
            [input_path],
            translator=translator,
        ).popitem()
        logger.info("writing %s", output_path)
        write_file(output_path, code)
        return

    if not output_path:
        output_path = input_path
    matches = match_files(input_path, r".*\.rpym?c$")
    file_codes = translate_files(
        input_path,
        matches,
        translator=translator,
        include_tl_lang=include_tl_lang,
        concurent=concurent,
    )
    for filename, code in file_codes.items():
        output_file = os.path.join(output_path, filename.removesuffix("c"))
        logger.info("writing %s", output_file)
        write_file(output_file, code)


def write_file(filename: str, data: str):
    """
    write data to file
    """
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)


def match_files(base_dir: str, pattern: str):
    """
    match files in dir with regex pattern

    Parameters
    ----------
    base_dir : str
        directory to find in
    pattern : str
        regex pattern

    Returns
    -------
    list[str]
        matched filenames relative to base_dir
    """

    if pattern == "":
        pattern = ".*"
    results = []
    matched = re.compile(pattern)
    for root, _, files in os.walk(base_dir):
        for filename in files:
            filename = os.path.relpath(os.path.join(root, filename), base_dir)
            if matched.match(filename):
                results.append(filename)
    return results


def read_rpyc_data(file: io.FileIO, slot):
    """
    Reads the binary data from `slot` in a .rpyc (v1 or v2) file. Returns
    the data if the slot exists, or None if the slot does not exist.
    """
    file.seek(0)
    header_data = file.read(1024)
    # Legacy path.
    if header_data[: len(RPYC2_HEADER)] != RPYC2_HEADER:
        if slot != 1:
            return None
        file.seek(0)
        data = file.read()
        return zlib.decompress(data)
    # RPYC2 path.
    pos = len(RPYC2_HEADER)
    while True:
        header_slot, start, length = struct.unpack("III", header_data[pos : pos + 12])
        if slot == header_slot:
            break
        if header_slot == 0:
            return None
        pos += 12
    file.seek(start)
    data = file.read(length)
    return zlib.decompress(data)


def load_file(filename, disasm: bool = False) -> renpy.ast.Node:
    """
    load renpy code from rpyc file and return ast tree.
    """
    ext = os.path.splitext(filename)[1]
    if ext in [".rpy", ".rpym"]:
        raise NotImplementedError(
            "unsupport for pase rpy file or use renpy.parser.parse() in renpy's SDK"
        )
    if ext in [".rpyc", ".rpymc"]:
        with open(filename, "rb") as file:
            for slot in [1, 2]:
                bindata = read_rpyc_data(file, slot)
                if bindata:
                    if disasm:
                        disasm_file = filename + ".disasm"
                        with open(disasm_file, "w", encoding="utf-8") as disasm_f:
                            pickletools.dis(bindata, out=disasm_f)
                    try:
                        _, stmts = pickle.loads(bindata)
                    except Exception as e:
                        logger.error("load %s failed: %s", filename, e)
                        raise e
                    return stmts
                file.seek(0)
    return None


def decompile_file(input_file, output_file=None):
    """
    decompile rpyc file into rpy file and write to output.
    """
    if not output_file:
        output_file = input_file.removesuffix("c")
    if not output_file.endswith(".rpy"):
        output_file = os.path.join(
            output_file, os.path.basename(input_file).removesuffix("c")
        )
    stmts = load_file(input_file)
    code = renpy.util.get_code(stmts)
    logger.info("writing %s", output_file)
    write_file(output_file, code)


def decompile(input_path, output_path=None):
    """
    decompile rpyc file or directory into rpy

    Parameters
    ----------
    input_path : str
        path to rpyc file or directory contains rpyc files
    output_path : str, optional
        output path, by default it's same path of input_path.
    """
    if not os.path.isdir(input_path):
        decompile_file(input_path, output_path)
        return
    if not output_path:
        output_path = input_path
    for filename in match_files(input_path, r".*\.rpym?c$"):
        decompile_file(
            os.path.join(input_path, filename),
            os.path.join(output_path, filename.removesuffix("c")),
        )


class DummyClass(object):
    """
    Dummy class for unpickling.
    """

    state = None

    def append(self, value):
        if self.state is None:
            self.state = []
        self.state.append(value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __eq__(self, __value: object) -> bool:
        pass

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getstate__(self):
        if self.state is not None:
            return self.state
        return self.__dict__

    def __setstate__(self, state):
        if isinstance(state, dict):
            self.__dict__ = state
        else:
            self.state = state


class GenericUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module.startswith("store") or module.startswith("renpy"):
            return type(name, (DummyClass,), {"__module__": module})
        return super().find_class(module, name)


def update_save(filename, update: Callable[[object], object] = lambda x: x):
    """
    decode renpy save file and update it with update function
    """
    with zipfile.ZipFile(filename, "r") as file:
        logdata = file.read("log")
    data = GenericUnpickler(io.BytesIO(logdata)).load()
    data = update(data)
    pickledata = pickle.dumps(data)
    with zipfile.ZipFile(filename, "r") as original_zip:
        with zipfile.ZipFile(filename + "_patched", "w") as new_zip:
            for item in original_zip.infolist():
                if item.filename != "log":
                    new_zip.write(item, original_zip.read(item.filename))
                else:
                    new_zip.write("log", pickledata)


def main():
    """
    command line tool entry.
    """
    logging.basicConfig(level=logging.INFO)
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--concurent", "-n", type=int, default=0, help="concurent translate"
    )
    argparser.add_argument(
        "--include-lang",
        "-i",
        default=None,
        help="add items in tl/<lang> dir to translations",
    )
    argparser.add_argument(
        "--verbose", "-v", action="store_true", help="verbose output"
    )
    argparser.add_argument(
        "--translate", action="store_true", help="decompile and translate"
    )
    argparser.add_argument("src", nargs=1, help="rpyc file or directory")
    argparser.add_argument("dest", nargs="?", help="output file or directory")
    args = argparser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    if args.translate:
        translate(
            args.src[0],
            args.dest,
            concurent=args.concurent,
            include_tl_lang=args.include_lang,
        )
    else:
        decompile(args.src[0], args.dest)


if __name__ == "__main__":
    main()
