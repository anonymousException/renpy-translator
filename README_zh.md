<div align=center><img src = "https://www.renpy.org/static/index-logo.png"></div>

# <div align=center>Renpy 翻译器</div>

<div align=center>一款免费开源的ren'py 翻译工具</div>

<div align=center><img src= "https://camo.githubusercontent.com/60c21c6ef57c61b0a329f621af32f87c9b4ffe0283eeebe8a453e60de2675c51/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f6c616d612d636c65616e6572"></div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/blob/main/docs/img/interface.png"></div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/blob/main/docs/img/translated_contents.png"></div>

------

## 目的

正如你所见上方翻译后的内容，在翻译后被翻译的原文也会被保留

如果要被翻译的内容缺少原内容(在"#"后作为注释)，那么这些内容将被跳过不被翻译

我做这个工具的目的不是为了替代人工翻译，而是帮助

翻译的内容通常因为机翻而不够准确

因此这时原文的作用就来了，你可以根据原文重写翻译，并且你修改后的内容也不会在后面的翻译里再被替换掉

本工具也处理了被翻译文本种包含特殊符号的场景，像 "{}"  "[]" 和 "<>" ，具体可以前往  [特性的第 2 点](#jump_features)

## 下载

你可以通过 https://github.com/anonymousException/renpy-translator/releases/latest 下载最新版本

## <span id = "jump_features">特性</span>

- 完全免费且开源
- 支持要翻译的文本中包含特殊符号，像 "{}"  "[]" 和 "<>"  , 特殊符号里的内容不会被翻译，例子：

  ```python
  # 未翻译的文本:
  # "Your name is [povname], right?"
  
  # 中文翻译:
  "你的名字是 [povname] ，对吗？"
  
  # 日语翻译:
  "あなたの名前は [povname] ですよね?"
  ```
- 支持抽取出 ren'py 未能发现的未翻译文本
- 支持输入、浏览、拖拽文件或者目录
- 支持针对单个 rpy 文件进行翻译/抽取未翻译文本
- 支持遍历某目录下的所有 rpy 进行翻译/抽取
- 支持**替换**要被翻译的语言的字体
- **兼容**未被该工具的翻译的翻译过的游戏 已经翻译过的原文会被保留，只翻译未翻译的内容
- 支持 **108 种**语言，具体的语言列表可参考： [源语言](https://github.com/anonymousException/renpy-translator/blob/main/src/source.rst?plain=1) 和 [目标(翻译后)的语言](https://github.com/anonymousException/renpy-translator/blob/main/src/target.rst?plain=1)
- 支持**保留**未被翻译的原本作为**注释**
- 支持 **实时日志输出** , 你可以随时观察当前的翻译进度
- 基于 Google 翻译 ，来源于 [pygtrans](https://github.com/foyoux/pygtrans/tree/main)

------

## 使用教程

### 事前准备

一个好的网络环境，如果网络不好，可能无法正常调用谷歌翻译来翻译

------

一个未被打包的 ren'py 游戏 (能够在游戏文件夹底下找到 .rpa 文件) ，如：

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unpacked.png)

你可以试试跟着这篇教程翻译我提供的 [教程游戏](https://github.com/anonymousException/renpy-translator/blob/main/docs/demo_game/DemoGame-1.0-win.zip)

如果游戏被打包了，需要解包：

我一般是用从  https://f95zone.to/ 整来的  [UnRen-ultrahack.bat ](https://github.com/anonymousException/renpy-translator/blob/main/docs/tool/UnRen-ultrahack.bat) 来解包

**强烈不推荐**翻译者通过解包翻译后未经原作者授权就私自发布翻译包，请**尊重**原作者

下载  [UnRen-ultrahack.bat]() 并把它拷贝到游戏目录底下 (里面含有 游戏名.exe)

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/move_unren.png)

双击 UnRen-ultrahack.bat 然后会弹出一个控制台

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unren_console.png)

输入 9 然后再输入 y

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unren_console2.png)

等一会以后就解包完成了

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unren_console3.png)

------

### 初次翻译

如果游戏完全没被翻译过，你可以接着看下面的内容

如果游戏已经被翻译过了(你想要再更新一下这个翻译) 可以直接跳转到  [翻译更新](#jump-update-translation)

要翻译的第一件事是抽取出要翻译的游戏文本

有 2 种方式:

- 官方抽取 (由 ren'py 引擎提供的官方方式)
- [本工具抽取](#jump-tool-extract) (由本工具提供的抽取方式)

推荐先 [官方抽取](#jump_official_extract) 翻译后发现翻译的文本不全时再使用本工具抽取补全后再翻译

#### <span id = "jump_official_extract">官方抽取(推荐) </span>

你可以前往 https://www.renpy.org/ 去下载最新版本的 ren'py 引擎

解压你下载的 ren'py 引擎

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_folder.png)

在右下角点击 "preferences"  (设置)

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_interface.png)

重新把 "Projects Directory" 设置为你要翻译游戏的上一层文件夹

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_preference.png)

返回上一个界面然后点击 "Generate Translations" (生成翻译)

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_interface2.png)

填写 "Lanauge" ， 这只是一个用来翻译的标签 (它相当于本工具里的 "tl name") ，你可以随便起名，但是最好用要被翻译的语言的名称来命名。比如 "japanese" 或 "chinese" 等

其他设置保持默认即可，注意 在 "Generate Translations"  (生成翻译) 里的 "Generate empty strings for translations" (为翻译生成空子串) 不要勾选

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_gen_translate.png)

当这些都设置好以后，点击 "Generate Translations"  (生成翻译) 然后等待翻译完成

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_gen_tranlate_over.png)

翻译完成以后就可以关闭软件了，官方抽取已经完成了

你可以看到生成好的文件夹，记住这个路径

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_gen_translate_folder.png)

教程里的路径是:

```
F:\Games\RenPy\DemoGame\game\tl\japanese
```

#### <span id = "jump-tool-extract"> 工具抽取(可选)</span>

填写(输入,拖拽或浏览) 前面 [官方抽取](#jump_official_extract) 生成的文件路径，然后点一下 extract 按钮，等待抽取完成即可

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_extract.png)

很简单,对吧？这就是我为什么做这个工具

#### 添加入口

你需要在游戏里添加一个用来切换语言的入口

打开游戏文件夹，然后再进入子目录 "game" ，打开 "screen.rpy" 文件 （可以用记事本打开）

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/screens.rpy_folder.png)

搜索关键字 : "game_menu(_("Preferences")" (一般这个关键字都是能搜到的，不然你就得自己找一下游戏用来替代 "Preferences" 的词)

通常来说你会找到很多 "vbox"，像这样:

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/screens_notepad.png)

尝试找到一个包含 "Language" 或其他 "Language" 的近义词的 vbox

如果没找到，把下面的代码粘贴到包含 "skip" 的 vbox 下面

```python
vbox:
    style_prefix "radio"
    label _("Language")
    textbutton "English" action Language(None) 
    textbutton "LanguageName" action Language("The Tag you fill in official Extract") 
    #比如 textbutton "turn to Japanese" action Language("japanese")
```

注意缩进保持对齐，在编辑后应该能得到类似:

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/screens_notepad_edit.png)

------

如果找到了，直接加一行到对应的 vbox 里

```python
textbutton "LanguageName" action Language("The Tag you fill in official Extract") 
#比如 textbutton "turn to Japanese" action Language("japanese")
```

------

当文件保存以后，打开游戏确保设置里面已经有了我们添加的切换语言的选项

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/game_language.png)

------

#### 翻译

翻译前你需要有一个能够正常显示你想要翻译的语言字体文件 (.*ttf or .otf)

对于日语，我一般是用 [hanazomefont](https://www.asterism-m.com/font/hanazomefont/) 这个字体

对于中文，我一般是用 [SourceHanSansSC-VF.otf](https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/OTF/SourceHanSansSC-VF.otf) 这个字体

对于其它语言，你可以很简单地在网上搜到相关的字体

打开本工具然后填写下面的内容

directory : 前面在[官方抽取](#jump_official_extract)生成得到的路径

font: 你下载的字体文件

target : 你想要翻译的语言 (支持输入单词的前缀字母来搜索 ,不用一直滑滚轮找)

source：默认 Auto Detect (自动检测) 就行

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_translate.png)

等待翻译完成：

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_translate_over.png)

到目前为止，翻译都完成了，你可以打开游戏检查一下

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/game_language_translated.png)

### <span id = "jump-update-translation"> 翻译更新 </span>

翻译更新很简单，直接使用 [官方抽取](#jump_official_extract) (可选) 和 [工具抽取](#jump-tool-extract)

抽取后，只需要输入前面在[官方抽取](#jump_official_extract)里生成的文件夹和选一下要翻译的语言  , font 可以留空，因为字体之前已经替换过了

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_update_translate.png)

## 开发

如果你想要基于本项目开发，你需要有一个 python3 的环境

然后安装的包体可以参考：[requirements.txt](https://github.com/anonymousException/renpy-translator/blob/main/src/requirements.txt)