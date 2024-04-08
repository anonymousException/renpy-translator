init python:
    import os
    import io
    import json
    renpy_runtime_extract_hook_file_name = 'extraction_hooked.json'
    translator = renpy.game.script.translator
    default_translates = translator.default_translates
    dic = dict()
    for identifier,value in default_translates.items():
        say = value.block[0]
        what = say.what
        who = say.who
        filename = value.filename
        linenumber = value.linenumber
        if filename not in dic:
            dic[filename] = [(identifier,who,what,linenumber)]
        else:
            dic[filename].append((identifier,who,what,linenumber))
    with io.open(renpy_runtime_extract_hook_file_name,'w',encoding="utf-8") as outfile:
        outfile.write(unicode(json.dumps(dic, ensure_ascii=False)))
    renpy.quit()