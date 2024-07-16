init python early hide:
    import os
    global importlib
    global inspect
    import importlib
    import inspect
    global check_function_exists
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

    global my_old_show_screen
    my_old_show_screen = renpy.show_screen
    global my_old_lookup
    my_old_lookup = None
    if check_function_exists('renpy.ast.Translate','lookup'):
        my_old_lookup = renpy.ast.Translate.lookup
    def my_show_screen(_screen_name, *_args, **kwargs):
        if _screen_name == 'preferences':
            _screen_name = 'my_preferences'
        if _screen_name == 'director':
            if my_old_lookup is not None:
                renpy.ast.Translate.lookup = my_old_lookup
        return my_old_show_screen(_screen_name, *_args, **kwargs)
    renpy.show_screen = my_show_screen

screen my_preferences():
    python:
        global os
        import os
        def traverse_first_dir(path):
            translator = renpy.game.script.translator
            languages = translator.languages
            l = languages
            if (os.path.exists(path)):
                files = os.listdir(path)
                for file in files:
                    m = os.path.join(path,file)
                    if (os.path.isdir(m)):
                        h = os.path.split(m)
                        l.add(h[1])
            return l
        l = traverse_first_dir('game/tl')
    tag menu
    use preferences
    vbox:
        align(.99, .99)
        hbox:
            box_wrap True
            vbox:
                label _("Language")
                textbutton "Default" action Language(None)
                $ cnt = 0
                for i in l:
                    if i is not None and i != 'None':
                        textbutton "%s" % i action Language(i)
