
<div align=center><img src = "https://www.renpy.org/static/index-logo.png"></div>

# <div align=center>Renpy Translator</div>

<div align=center>A free and open-source translator for ren'py</div>

<div align=center><img src= "https://camo.githubusercontent.com/60c21c6ef57c61b0a329f621af32f87c9b4ffe0283eeebe8a453e60de2675c51/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f6c616d612d636c65616e6572"></div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/blob/main/docs/img/interface_v1.2.0.png"></div>

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/blob/main/docs/img/translated_contents.png"></div>

------

## Another Docs

## AI Version

If you want to use offline ai translation, you can refer to :

https://github.com/anonymousException/renpy-translator/blob/feature/ai-translate/README.md

### Chinese

<div align=center>中文版 README 在 <a href = 'https://github.com/anonymousException/renpy-translator/blob/main/README_zh.md'>这里</a> </div>

## Target

As you see the above translated contents. The original contents will be remained after translation.

If the contents are short of the original contents(behind the "#" as comment) , translation will not take effect on them

The reason why I made this tool is not to replace the real translator's work , but to help.

The translated contents will be not accurate enough due to auto google translation. 

So the original contents will do the effect. You can re-translate the translated contents according to the original contents. And what you modified will not be replaced during next translation.

This tool also take care of the special symbols like "{}"  "[]" and "<>"   in untranslated contents , for detail you can see it on the [Features point 2](#jump_features)

## Download

You can download the latest version through https://github.com/anonymousException/renpy-translator/releases/latest

## <span id ="jump_features">Features</span>

- Completely free and open-source
- Support **special symbols** in untranslated contents like "{}"  "[]" and "<>"  , the contents in special symbols will not be translated.  Example:
- ```python
  # untranslated contents:
  # "Your name is [povname], right?"
  
  # Chinese translated:
  "你的名字是 [povname] ，对吗？"
  
  # Japanese translated:
  "あなたの名前は [povname] ですよね?"
  ```

- Support  extract the untranslated words ren'py engine has not discovered
- Support input,brower and drag the file(s) and directory
- Support translate/extract for single rpy file
- Support translate/extract for all rpy files under directory
- Support **replace the fonts** used by translated language
- Support **be compatible with** the translated game that not translated by this translator. The translated contents before will be remained and just translate the untranslated contents
- Support **108** kinds of language , you can view the [support source](https://github.com/anonymousException/renpy-translator/blob/main/src/source.rst?plain=1) and the [support target](https://github.com/anonymousException/renpy-translator/blob/main/src/target.rst?plain=1)
- Support **remain the original words as comments** after translation
- Support **real-time log output** , you can check the progress about the translation
- Based on Google Translation from [pygtrans](https://github.com/foyoux/pygtrans/tree/main)

------

## Usage

Translate Files:

https://github.com/anonymousException/renpy-translator/assets/157234942/495be06c-9751-4966-b22c-84602fb3dc0a

Translate Directory:

https://github.com/anonymousException/renpy-translator/assets/157234942/0034bbaa-d1fc-4981-b228-9bde62423367

Replace fonts:

https://github.com/anonymousException/renpy-translator/assets/157234942/46e524d7-14ef-472e-8426-ac47d923bef0

Extract Directory:

https://github.com/anonymousException/renpy-translator/assets/157234942/817c6e9c-2fa2-48a3-914f-85765c0b64c3

## Tutorial

### Prerequisite

A good network environment , if not you may not able to translate words through ***Google Translate***

------

An unpacked ren‘py game (for what you can find .rpa files under the game directory)  like this:

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unpacked.png)

You can try to translate [the tutorial game](https://github.com/anonymousException/renpy-translator/blob/main/docs/demo_game/DemoGame-1.0-win.zip) following the tutorial

if not you can try to unpack it

I usually use [UnRen-ultrahack.bat](https://github.com/anonymousException/renpy-translator/blob/main/docs/tool/UnRen-ultrahack.bat) from https://f95zone.to/ to unpack the game

It's **strongly not recommended** for translators to make translation through unpack and then deliver a translated version without the original author's permission. Please **respect** the original author

Download the  [UnRen-ultrahack.bat]() and copy it to the game directory (where game.exe locates)

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/move_unren.png)

Double-Click the UnRen-ultrahack.bat and the following console will show

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unren_console.png)

Input 9 and then Enter and then Enter y

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unren_console2.png)

Wait for a moment and then the unpack will be over

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unren_console3.png)

------

### FirstTranslation

If the game is completely blend-new for you to translate , you can continue to the following contents

If the game has already been translated , you want to update the translation (translate the contents still not been translated) , you can jump to the next caption :  [UpdateTranslation](#jump-update-translation)

the first thing for the First-Translation is to extract the untranslated words from game

there are two methods to do that:

- Official Extract (extract function supported by the ren'py engine)
- [Tool Extract](#jump-tool-extract) (extract function supported by this tool)

It's recommended to use [Offical Extract](#jump_official_extract) first and then translate the game. If you found that there still remains plenty of words not been translated after translation (Sometimes ren'py engine's official extract may miss many words). You can use the tool extract function and retranslate the game.

#### <span id = "jump_official_extract">Official Extract(Recommend) </span>

https://github.com/anonymousException/renpy-translator/assets/157234942/b032480f-fc2f-4438-9730-611b3e219556

you can forward to https://www.renpy.org/ and then download the latest version

Unzip the ren'py engine you download

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_folder.png)

Click "preferences" in the lower right corner

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_interface.png)

Reset the "Projects Directory" to the parent directory of the game you want to translate

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_preference.png)

Return back to the last interface and Click "Generate Translations"

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_interface2.png)

Fill the "Language" , this is just a tag (It's related to the "tl name" label in this tool) used for the translation that you can name whatever you want. But it's recommended to name the target language you want to translate. Such as "japanese" or "chinese" etc.

It would be alright to keep other options default ,Especially for "Generate Translations" option , do not tick the "Generate empty strings for translations"

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_gen_translate.png)

After all options have been set . Click the "Generate Translations" and wait to complete

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_gen_tranlate_over.png)

And then you can close the software , the official extract is done

You can see the generated folder , remember the path

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_gen_translate_folder.png)

The folder path in this tutorial is : 

```
F:\Games\RenPy\DemoGame\game\tl\japanese
```

#### <span id = "jump-tool-extract"> Tool Extract(Optional)</span>

Fill (input,drag or brower) the directory that generated by [Official Extract](#jump_official_extract) before and just tap the extract buttion , and then extraction will be done

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_extract.png)

Quite easy, right ? That's why I made this tool.

#### Add Entry

https://github.com/anonymousException/renpy-translator/assets/157234942/a0316ab5-f912-4e25-8423-19b82b7fbfbe

You need to add an entry to change the language in game

Open the game directory and then enter subfolder "game", open the "screens.rpy" file (you can use notepad to open it)

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/screens.rpy_folder.png)

Search the key words："game_menu(_("Preferences")" (usually the words do effect if not you may need to explore what the game use to replace "Preferences")

Normally you will found many "vbox:" like this:

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/screens_notepad.png)

Try to find a vbox that contains "Language" or some other words can replace "Language"

If not found , add the following code to the file(the location next to the vbox contains "skip"):

```python
vbox:
    style_prefix "radio"
    label _("Language")
    textbutton "English" action Language(None) 
    textbutton "LanguageName" action Language("The Tag you fill in official Extract") 
    #such as textbutton "turn to Japanese" action Language("japanese")
```

Pay attention to the indentation to keep it aligned. After edit it should be like this

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/screens_notepad_edit.png)

------

If found , just add a new line to the vbox:

```python
textbutton "LanguageName" action Language("The Tag you fill in official Extract") 
#such as textbutton "turn to Japanese" action Language("japanese")
```

------

After the file saved,open the game and make sure the preference show the content you just edit

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/game_language.png)

------

#### Translation

https://github.com/anonymousException/renpy-translator/assets/157234942/9b1c0b9f-7f90-4a90-9876-6588994d0658

Before translation you need to get the font file (.*ttf or .otf) you want to translate

For japanese, I usually use the [hanazomefont](https://www.asterism-m.com/font/hanazomefont/)

For chinese, I usally use the [SourceHanSansSC-VF.otf](https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/OTF/SourceHanSansSC-VF.otf)

For other language , you can find relative font files using search engine easily

Open the ren'py translator and fill the following blanks

directory : the path  generated during [Official Extract](#jump_official_extract) before

font: the font file you downloaded

target : the target language you want to translate (input the letter in front of the target language to search  is supportable , need not to scroll to search)

source: default Auto Detect is OK

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_translate.png)

Wait until the translation done:

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_translate_over.png)

So far , the translation is done , you can open game and check it : 

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/game_language_translated.png)

### <span id = "jump-update-translation"> UpdateTranslation </span>

Update-Translation is quite easy, directly use the [Official Extract](#jump_official_extract) (optional) and [Tool Extarct](#jump-tool-extract)

After extraction ,  just input the directory generated during [Official Extract](#jump_official_extract) and choose the target , font can leave empty because it has been replaced before

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_update_translate.png)

## Development

If you are willing to develop based on this project. You will need to have a python3 environment.

And install the following packages ：[requirements.txt](https://github.com/anonymousException/renpy-translator/blob/main/src/requirements.txt)
