import io
import os
import subprocess

from call_game_python import get_python_path_from_game_path, get_py_path
from my_log import log_print
from renpy_extract import remove_repeat_for_file, get_remove_consecutive_empty_lines

lint_out_path = 'error_repair.txt'


def get_renpy_cmd(game_path):
    python_path = get_python_path_from_game_path(game_path)
    py_path = get_py_path(game_path)
    game_dir = os.path.dirname(game_path)

    command = '"' + python_path + '"' + ' -O "' + py_path + '" "' + game_dir + '" lint ' + '"' + os.path.dirname(
        game_path) + '/' + lint_out_path + '"' + ' >> ' + '"' + os.path.dirname(
        game_path) + '/' + lint_out_path[:-4] + '.error.txt"'
    return command


def exec_renpy_lint(game_path):
    command = get_renpy_cmd(game_path)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         creationflags=0x08000000, text=True, encoding='utf-8')
    p.wait()


def fix_translation_by_lint(game_path):
    target = os.path.dirname(game_path) + '/' + lint_out_path
    if os.path.isfile(target):
        os.remove(target)
    exec_renpy_lint(game_path)
    if os.path.isfile(target):
        os.remove(target)
        target = target[:-4] + '.error.txt'
        if os.path.isfile(target):
            os.remove(target)
        return False
    target = target[:-4] + '.error.txt'
    if not os.path.isfile(target):
        return False
    f = io.open(target, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    os.remove(target)
    log_print('renpy lint finish, start analyzing...')
    is_fixed = False
    fix_list = []
    for line in lines:
        line = line.rstrip('\n')
        err_file = ''
        err_line = -1
        if (line.endswith('is not terminated with a newline. (Check strings and parenthesis.)') or line.endswith(
                'end of line expected.')
                or line.endswith('expects a non-empty block.') or line.endswith('unknown statement')
                or line.endswith('expected statement.')) or line.endswith('Could not parse string.'):
            idx = line.index(', line ')
            err_file = line[line.index(' ') + 1:idx].strip('"')
            err_line = line[idx + len(', line '): line.index(':', idx)].strip()
            err_line = int(err_line) - 1
            if line in fix_list:
                continue
            fix_list.append(line)
        if line.startswith('Exception: A translation for '):
            idx = line.rindex('already exists at ')
            err_content = line[len('Exception: A translation for '):idx].rstrip()
            idx = idx + len('already exists at ')
            err_info = line[idx:].rstrip('.').lstrip()
            err_file, err_line = err_info.split(':', 1)
            err_line = int(err_line) + 1
            if err_info in fix_list:
                continue
            fix_list.append(err_info)
        if err_line == -1:
            continue
        err_file = os.path.dirname(game_path) + '/' + err_file
        if not os.path.isfile(err_file):
            log_print('error path : ' + err_file)
        f = io.open(err_file, 'r', encoding='utf-8')
        _lines = f.readlines()
        f.close()
        if err_line >= len(_lines):
            continue
        log_print(
            'remove error line ' + str(err_line) + ' in ' + err_file + ' : "' + _lines[err_line].rstrip('\n') + '"')
        if _lines[err_line - 1].rstrip().endswith('""")'):
            _idx = err_line
            new_idx = -1
            end_idx = -1
            while True:
                if _idx >= len(_lines):
                    break
                if _lines[_idx].startswith('    new _p("""'):
                    new_idx = _idx
                    break
                _idx = _idx - 1
            if new_idx != -1:
                _idx = new_idx - 1
                while True:
                    if _idx >= len(_lines):
                        break
                    if _lines[_idx].startswith('    old _p("""'):
                        end_idx = _idx
                        break
                    _idx = _idx - 1
            if end_idx != -1:
                for _idx in range(end_idx, err_line + 1):
                    _lines[_idx] = '\n'

        elif _lines[err_line].startswith('    old ') and _lines[err_line + 1].startswith('    new '):
            _lines[err_line] = ''
            _lines[err_line + 1] = ''
            if _lines[err_line - 1].lstrip().startswith('#'):
                _lines[err_line - 1] = ''
        elif _lines[err_line].startswith('    new ') and _lines[err_line - 1].startswith('    old '):
            _lines[err_line] = ''
            _lines[err_line - 1] = ''
            if _lines[err_line - 2].lstrip().startswith('#'):
                _lines[err_line - 2] = ''
        elif line.endswith('unknown statement') or line.endswith('expected statement.'):
            _lines[err_line] = '\n'
        else:
            if _lines[err_line].startswith('translate'):
                _lines[err_line] = '\n'
            else:
                _lines[err_line] = '    ""\n'
        f = io.open(err_file, 'w', encoding='utf-8')
        _lines = get_remove_consecutive_empty_lines(_lines)
        f.writelines(_lines)
        f.close()
        is_fixed = True
    return is_fixed


def fix_translation_by_lint_recursion(game_path, max_recursion_depth):
    command = get_renpy_cmd(game_path)
    log_print(command)
    cnt = 0
    while True:
        log_print('start reparing ' + str(cnt + 1) + '/' + str(max_recursion_depth))
        if not fix_translation_by_lint(game_path):
            log_print('no errors left, finish!')
            break
        cnt = cnt + 1
        if cnt >= max_recursion_depth:
            break

# fix_translation_by_lint_recursion('F:/Games/RenPy/DemoGame-1.1-dists/DemoGame-1.1-win/DemoGame.exe' , 16)
