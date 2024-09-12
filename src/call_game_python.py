import io
import os
import platform
import shutil
import subprocess


def is_64_bit():
    return platform.architecture()[0] == '64bit'


def get_python_path_from_game_dir(game_dir):
    lib_list_64 = ['windows-x86_64', 'py2-windows-x86_64', 'py3-windows-x86_64']
    lib_list_86 = ['windows-i686', 'py2-windows-i686', 'py3-windows-i686']
    python_path = None
    if is_64_bit():
        lib_list_64.extend(lib_list_86)
        for i in lib_list_64:
            target = game_dir + 'lib/' + i + '/python.exe'
            if os.path.isfile(target):
                python_path = target
                break
    else:
        for i in lib_list_86:
            target = game_dir + 'lib/' + i + '/python.exe'
            if os.path.isfile(target):
                python_path = target
                break
    return python_path


def get_python_path_from_game_path(game_path):
    game_dir = os.path.dirname(game_path) + '/'
    return get_python_path_from_game_dir(game_dir)


def is_python2_with_python_dir(python_dir):
    paths = os.walk(python_dir, topdown=False)
    is_py2 = False
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if 'python2' in i or 'py2' in i:
                is_py2 = True
                break
    return is_py2


def is_python2_from_game_dir(game_dir):
    try:
        python_dir = os.path.dirname(get_python_path_from_game_dir(game_dir))
    except Exception:
        return True
    return is_python2_with_python_dir(python_dir)


def is_python2_from_game_path(game_path):
    try:
        python_dir = os.path.dirname(get_python_path_from_game_path(game_path))
    except Exception:
        return True
    return is_python2_with_python_dir(python_dir)


def get_py_path(game_path):
    base_name = os.path.splitext(game_path)[0]
    return base_name + '.py'


def copy_files_under_directory_to_directory(src_dir, desc_dir):
    shutil.copytree(src_dir, desc_dir, dirs_exist_ok=True)


def get_game_path_from_game_dir(game_dir):
    for item in os.listdir(game_dir):
        full_path = os.path.join(game_dir, item)
        if os.path.isfile(full_path) and item.lower().endswith('.exe'):
            if os.path.isfile(full_path[:-len('.exe')] + '.py'):
                return full_path
    return None
