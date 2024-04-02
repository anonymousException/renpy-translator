init python early hide:
    import os
    my_old_show_screen = renpy.show_screen
    my_old_lookup = renpy.ast.Translate.lookup
    def my_show_screen(_screen_name, *_args, **kwargs):
        if _screen_name == 'preferences':
            _screen_name = 'my_preferences'
        if _screen_name == 'director':
            renpy.ast.Translate.lookup = my_old_lookup
        return my_old_show_screen(_screen_name, *_args, **kwargs)
    renpy.show_screen = my_show_screen

screen my_preferences():
    python:
        def traverse_first_dir(path):
            l = []
            if (os.path.exists(path)):
                files = os.listdir(path)
                for file in files:
                    m = os.path.join(path,file)
                    if (os.path.isdir(m)):
                        h = os.path.split(m)
                        l.append(h[1])
            return l
        l = traverse_first_dir('game/tl')
    tag menu
    use preferences
    vbox:
        align(.99, .99)
        hbox:
            box_wrap True
            vbox:
                style_prefix "radio"
                label _("Language")
                textbutton "Default" action Language(None)
                for i in range(len(l)):
                    if l[i] == 'None':
                        continue
                    textbutton "%s" % l[i] action Language(l[i])