import io
import os
import platform
import shutil
import subprocess


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


def get_python_version(game_path):
    command = get_python_path(game_path) + ' -O --version'
    f = io.open(os.getcwd() + '/tmp_python_version.txt', 'w', encoding='utf-8')
    p = subprocess.Popen(command, shell=True, stdout=f, stderr=f,
                         creationflags=0x08000000, text=True, encoding='utf-8')
    p.wait()
    f.close()
    f = io.open(os.getcwd() + '/tmp_python_version.txt', 'r', encoding='utf-8')
    python_version = f.read()
    f.close()
    os.remove(os.getcwd() + '/tmp_python_version.txt')
    return python_version


def is_python2(game_path):
    return get_python_version(game_path).startswith('Python 2.')


def get_py_path(game_path):
    base_name = os.path.splitext(game_path)[0]
    return base_name + '.py'


def copy_files_under_directory_to_directory(src_dir, desc_dir):
    shutil.copytree(src_dir, desc_dir, dirs_exist_ok=True)

