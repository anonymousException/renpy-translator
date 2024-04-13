import os
import platform


def is_64_bit():
    return platform.architecture()[0] == '64bit'


def get_python_path(game_path):
    game_dir = os.path.dirname(game_path) + '/'
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


def get_py_path(game_path):
    base_name = os.path.splitext(game_path)[0]
    return base_name + '.py'