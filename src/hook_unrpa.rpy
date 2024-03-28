init python early hide:
    import renpy.loader
    import threading
    from renpy.loader import file_open_callbacks,load_from_archive,SubFile

    def my_load_from_archive(name):
        rv = load_from_archive(name)
        if rv is None:
            return rv
        if isinstance(rv,SubFile):
            _read = rv.read()
        elif 'RWops' in str(type(rv)):
            _read = rv.readall()
        else:
            return rv
        file_open_callbacks.remove(my_load_from_archive)
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
            # use this to mark whether the rpa file is extracted
            renpy.loader.load_from_apk = None
            file.write(_read)
            if path.endswith((".rpyc", ".rpymc")) and not target_dir.endswith("None") and not base_name=='common':
                print(path)

        rv = load_from_archive(name)
        file_open_callbacks.append(my_load_from_archive)
        return rv

    file_open_callbacks.remove(load_from_archive)

    file_open_callbacks.append(my_load_from_archive)



init python:
    import os
    my_old_show_screen = renpy.show_screen

    def my_show_screen(_screen_name, *_args, **kwargs):
        finish_flag = 'unpack.finish'
        if renpy.loader.load_from_apk == None:
            if os.path.isfile(finish_flag):
                os.remove(finish_flag)
            renpy.quit()
        else:
             if os.path.isfile(finish_flag):
                os.remove(finish_flag)
        renpy.show_screen = my_old_show_screen
        return my_old_show_screen(_screen_name, *_args, **kwargs)

    renpy.show_screen = my_show_screen