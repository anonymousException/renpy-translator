init python early hide:
    import renpy.loader
    import threading
    import io
    from renpy.loader import file_open_callbacks,load_from_archive,archives

    def my_load_from_archive(name):
        try:
            rv = load_from_archive(name)
        except:
            print('load_from_archive : ' + name +' error!')
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
        #file_open_callbacks.remove(my_load_from_archive)
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
            if path.endswith((".rpyc", ".rpymc")) and not target_dir.endswith("None") and not base_name=='common':
                if path is not None and isinstance(path,str):
                    print(path)

        rv = load_from_archive(name)
        #file_open_callbacks.append(my_load_from_archive)
        return rv

    #file_open_callbacks.remove(load_from_archive)

    #file_open_callbacks.append(my_load_from_archive)

    for prefix, index in archives:
        for name in index.keys():
            print(name)
            my_load_from_archive(name)

    finish_flag = 'unpack.finish'
    if os.path.isfile(finish_flag):
        os.remove(finish_flag)