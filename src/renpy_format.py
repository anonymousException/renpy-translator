# -*- coding: utf-8
import io
import os
import threading
import traceback

from my_log import log_print

format_threads = []

lock = threading.Lock()


class formatThread(threading.Thread):
    def __init__(self, p, dirs):
        threading.Thread.__init__(self)
        self.p = p
        self.dirs = dirs

    def run(self):
        try:
            if self.p is not None:
                self.p = self.p.replace('\\', '/')
                log_print(self.p + ' begin format!')
                format_rpy(self.p)

            if self.dirs is not None:
                for _dir in self.dirs:
                    _dir = _dir.replace('\\', '/')
                    _dir = _dir.rstrip('/')
                    log_print(_dir + ' begin format!')
                    paths = os.walk(_dir, topdown=False)
                    t_list = []
                    for path, dir_lst, file_lst in paths:
                        for file_name in file_lst:
                            i = os.path.join(path, file_name)
                            if not file_name.endswith("rpy"):
                                continue
                            t = formatThread(p=i, dirs=None)
                            format_threads.append(t)
                            t_list.append(t)
                            t.start()
                    for t in t_list:
                        t.join()
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


def format_rpy(p):
    try:
        f = io.open(p, 'r', encoding='utf-8')
    except:
        log_print(p + ' file not found')
        return
    try:
        size = os.path.getsize(p)
        _read = f.read()
        f.close()
    except:
        f.close()
        return
    try:
        _new_line = _read.split('\n')
        _read_line = _read.split('\n')
        _len = len(_read_line)
        index = 0
        format_count = 0
        format_line_list = []
        while index < _len:
            line_content = _read_line[index]
            if line_content.startswith('translate '):
                split_s = line_content.split(' ')
                if len(split_s) > 2:
                    target = split_s[2].strip('\n')
                    if target != 'python:' and target != 'style':
                        _next = index + 1
                        while _next < _len:
                            if _read_line[_next].startswith('translate '):
                                break
                            _next = _next + 1
                        content_index = -1
                        for _index in range(index + 1, _next):
                            if len(_read_line[_index].strip('\n')) > 0:
                                if content_index == -1:
                                    content_index = _index
                                else:
                                    content_index = -1
                                    break
                        if content_index != -1:
                            # log_print(_read_line[content_index])
                            comment = '    # ' + _read_line[content_index].lstrip(' ')
                            _new_line.insert(format_count + content_index, comment)
                            format_line_list.append(format_count + content_index)
                            format_count = format_count + 1
                        index = _next - 1

            index = index + 1
        log_print(f'{p} format {format_count} lines')
        for i in range(len(_new_line)):
            _new_line[i] = _new_line[i] + '\n'
        f = io.open(p, 'w', encoding='utf-8')
        f.writelines(_new_line)
        f.close()
    except:
        msg = traceback.format_exc()
        log_print(msg)
