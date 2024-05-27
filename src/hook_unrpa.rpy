init python early hide:
    import renpy.loader
    import threading
    import io
    import importlib
    import inspect
    import os
    from renpy.loader import archives

    def check_function_exists(module_name, function_name):
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            if inspect.isfunction(function):
                #print(f"The function '{function_name}' exists in the module '{module_name}'.")
                return True
            else:
                #print(f"The name '{function_name}' exists in the module '{module_name}', but it is not a function.")
                return False
        except ImportError:
            #print(f"The module '{module_name}' does not exist.")
            return False
        except AttributeError:
            #print(f"The function '{function_name}' does not exist in the module '{module_name}'.")
            return False

    def my_load_from_archive(name):
        load_packed_file_source = None
        if check_function_exists('renpy.loader','load_from_archive'):
            from renpy.loader import load_from_archive as load_packed_file
            load_packed_file_source = 'load_from_archive'
        elif check_function_exists('renpy.loader','load_core'):
            from renpy.loader import load_core as load_packed_file
            load_packed_file_source = 'load_core'
        else:
            print('Error! Can not locate load_packed_file function!')
            return None
        try:
            rv = load_packed_file(name)
        except:
            print(load_packed_file_source + ' : ' + name +' error!')
            return None
        if rv is None:
            return rv
        if hasattr(renpy.loader,"SubFile") and isinstance(rv,renpy.loader.SubFile):
            _read = rv.read()
        elif isinstance(rv,io.BufferedReader):
            _read = rv.read()
        elif 'RWops' in str(type(rv)):
            _read = rv.readall()
        else:
            return rv

        current_file_path = os.path.abspath(sys.argv[0])
        current_dir_path = os.path.dirname(current_file_path)
        path = current_dir_path + '/game/' + name
        target_dir = os.path.dirname(path)
        base_name = os.path.basename(os.path.splitext(path)[0])
        if not os.path.exists(target_dir):
            if sys.version > '3':
                os.makedirs(target_dir,exist_ok=True)
            else:
                os.makedirs(target_dir)
        with open(path, 'wb') as file:
            file.write(_read)
            print(path)

        rv = load_packed_file(name)
        return rv

    for prefix, index in archives:
        for name in index.keys():
            #print(name)
            my_load_from_archive(name)

    finish_flag = 'unpack.finish'
    pid_flag = 'game.pid'
    f = io.open(pid_flag, 'w',encoding='utf-8')
    if sys.version > '3':
        f.write(str(os.getpid()))
    else:
        f.write(str(os.getpid()).decode('utf-8'))
    f.close()
    if os.path.isfile(finish_flag):
        os.remove(finish_flag)