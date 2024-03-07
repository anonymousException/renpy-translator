<div align=center><img src = "https://www.renpy.org/static/index-logo.png"></div>

# <div align=center>Renpy 翻译器</div>

<div align=center>一款免费开源的ren'py 翻译工具</div>

<div align=center><img src= "https://camo.githubusercontent.com/60c21c6ef57c61b0a329f621af32f87c9b4ffe0283eeebe8a453e60de2675c51/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f6c616d612d636c65616e6572"></div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/blob/main/docs/img/interface_v1.8.0.png"></div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/blob/main/docs/img/translated_contents.png"></div>

------

## 其他文档

### 离线 AI 版

如果你想要使用离线 AI 翻译，请前往：

https://github.com/anonymousException/renpy-translator/blob/feature/ai-translate/README_zh.md

## 支持的翻译引擎

| Translator                                                   | Supported Language number | Charge                 | Service                                                      | Country | Reference                                                |
| ------------------------------------------------------------ | ------------------------- | ---------------------- | ------------------------------------------------------------ | ------- | -------------------------------------------------------- |
| [Google](https://cloud.google.com/translate/docs/quickstarts) | 108                       | Free \| Token Required | [ Google](https://about.google/),                            | America | [pygtrans](https://github.com/foyoux/pygtrans/tree/main) |
| [Youdao](https://ai.youdao.com/doc.s#guide)                  | 11 \| 114                 | Free \| Token Required | [Netease](https://ir.netease.com/company-overview/corporate-profile) | China   |                                                          |
| [Deepl](https://www.deepl.com/account/?utm_source=github&utm_medium=github-python-readme) | 29                        | Token Required         | [Deepl](https://jobs.deepl.com/l/en)                         | Germany |                                                          |
| [OpenAI](https://platform.openai.com/api-keys)               | 108                       | Token Required         | [OpenAI](https://platform.openai.com/)                       | America | [openai-python](https://github.com/openai/openai-python) |
| [Alibaba](https://translate.alibaba.com)                     | 214                       | Free                   | [damo](https://damo.alibaba.com/about?tab=0&language=zh)     | China   | [translators](https://github.com/UlionTse/translators)   |
| [ModernMt](https://www.modernmt.com/translate)               | 200                       | Free                   | [Modernmt](https://github.com/modernmt) / [Translated](https://translatedlabs.com/welcome) | Italy   | [translators](https://github.com/UlionTse/translators)   |
| [Bing](https://www.bing.com/Translator)                      | 133                       | Free                   | [Modernmt](https://github.com/modernmt) / [Translated](https://translatedlabs.com/welcome) | Italy   | [translators](https://github.com/UlionTse/translators)   |
| [lingvanex](https://lingvanex.com/demo)                      | 109                       | Free                   | [Lingvanex](https://lingvanex.com/about-us/),                | Cyprus  | [translators](https://github.com/UlionTse/translators)   |
| [CloudTranslation](https://www.cloudtranslation.com/#/translate) | 8                         | Free                   | [Xiamen University](http://nlp.xmu.edu.cn/) / [CloudTranslation](https://www.cloudtranslation.com/#/about) | China   | [translators](https://github.com/UlionTse/translators)   |
| [Caiyun](https://fanyi.caiyunapp.com/)                       | 7                         | Free                   | [ColorfulClouds](http://caiyunapp.com/jobs/)                 | China   | [translators](https://github.com/UlionTse/translators)   |

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
- 支持**跳过**已抽取过的内容 , 不用担心**重复**抽取

  举个例子 ,如果翻译内容已经存在于 tl 目录下

  如:

  ```python
  old "Hello"
  new "こんにちは"
  ```

  或:

  ```python
  # game/xxx.rpy:1352
  translate japanese role_lose_7489b947:
  
      # "Hello"
      "こんにちは"
  ```

  那么 "Hello" 将不会再被抽取
- 支持 **108 种**语言(默认的谷歌翻译)，具体的语言列表可参考： [谷歌源语言](https://github.com/anonymousException/renpy-translator/blob/main/src/google.source.rst?plain=1) 和 [谷歌目标(翻译后)的语言](https://github.com/anonymousException/renpy-translator/blob/main/src/google.target.rst?plain=1)
- 支持**保留**未被翻译的原文本作为**注释**
- 支持**实时日志输出** , 你可以随时观察当前的翻译进度
- 支持**本地代理**，如果你不能正常访问谷歌|有道|Deepl，可以尝试使用 VPN (如 V2ray) 并配置本地代理
- 支持**多种**翻译引擎 

------

## 用法

翻译(多)文件:

https://github.com/anonymousException/renpy-translator/assets/157234942/495be06c-9751-4966-b22c-84602fb3dc0a

翻译整个文件夹:

https://github.com/anonymousException/renpy-translator/assets/157234942/0034bbaa-d1fc-4981-b228-9bde62423367

替换字体:

https://github.com/anonymousException/renpy-translator/assets/157234942/46e524d7-14ef-472e-8426-ac47d923bef0

抽取(多个)文件:

https://github.com/anonymousException/renpy-translator/assets/157234942/7d1efbfd-7152-407f-9896-c63a98538f02

抽取(多个)文件夹

https://github.com/anonymousException/renpy-translator/assets/157234942/518e34a9-12f6-4e69-9ac4-80a6b181081c

抽取所有内容到整个 tl 目录并重命名(如果 tl name 为空则直接抽取到输入的 tl 目录下):

https://github.com/anonymousException/renpy-translator/assets/157234942/09edf9fa-0f5c-410a-acd9-6fd219b55893

## 使用教程

### 事前准备

一个好的网络环境，如果网络不好，可能无法正常调用**翻译引擎**来翻译

当你发现无法正常访问谷歌翻译时，可以试试：https://github.com/GoodCoder666/GoogleTranslate_IPFinder

使用工具替换完 host 以后再尝试翻译 (该方法不一定有效，很大程度上取决于当地网络运营商)

或者使用本地代理功能：

使用前：

![proxy_fail](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/proxy_fail.png)

使用：

![proxy_setting](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/proxy_setting.png)

------

一个未被打包的 ren'py 游戏 (能够在游戏文件夹底下找到 .rpa 文件) ，如：

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/unpacked.png)

你可以试试跟着这篇教程翻译我提供的 [教程游戏](https://github.com/anonymousException/renpy-translator/blob/main/docs/demo_game/DemoGame-1.0-win.zip)

如果游戏被打包了，需要解包：

我一般是用从  https://f95zone.to/ 整来的  [UnRen-ultrahack.bat ](https://github.com/anonymousException/renpy-translator/blob/main/docs/tool/UnRen-ultrahack.bat) 来解包

https://github.com/anonymousException/renpy-translator/assets/157234942/718b2b71-ca98-4dfd-999b-ffdc9c112102

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

https://github.com/anonymousException/renpy-translator/assets/157234942/b032480f-fc2f-4438-9730-611b3e219556

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

https://github.com/anonymousException/renpy-translator/assets/157234942/a0316ab5-f912-4e25-8423-19b82b7fbfbe

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

https://github.com/anonymousException/renpy-translator/assets/157234942/46e524d7-14ef-472e-8426-ac47d923bef0

翻译前你需要有一个能够正常显示你想要翻译的语言字体文件 (.*ttf or .otf)

对于日语，我一般是用 [hanazomefont](https://www.asterism-m.com/font/hanazomefont/) 这个字体

对于中文，我一般是用 [SourceHanSansCN](https://github.com/CyanoHao/WFM-Free-Font/tree/master/SourceHanSansCN) 这个字体

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

抽取后，只需要输入前面在[官方抽取](#jump_official_extract)里生成的文件夹和选一下要翻译的语言 

对于字体，如果更新后的游戏新增了特殊的 style (有不同的字体设置)  , 你可以使用字体替换功能时不输入字体的路径来涵盖新增的那部分特殊 styles （字体先前已经替换过了）

![img](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/renpy_translator_update_translate.png)

## 开发

如果你想要基于本项目开发，你需要有一个 python3 的环境

然后安装的包体可以参考：[requirements.txt](https://github.com/anonymousException/renpy-translator/blob/main/src/requirements.txt)

## 问题和解答

### 翻译全都被跳过了

![skip](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/translation_all_skip.png)

确保在 [官方抽取](#jump_official_extract) 环节, 对于 "Generate Translations" (生成翻译) 选项, 不要勾选 "Generate empty strings for translations"(为翻译生成空子串)

翻译只会在满足下面格式时生效:

```python
# game/script.rpy:553
translate schinese naming_0f7b6e71:
	# r "Do name yourself like that and I'll break your face..."
	r "Do name yourself like that and I'll break your face..."
```

or

```python
    # game/script.rpy:30886
    old "Win or Lose?"
    new "Win or Lose?"
```

------

注意原始文本(在 # 或 old 后) 应该和未翻译的文本(在非 # 或 new 后)**完全一样**

------

### <span id = "jump_error_translate_special_symbols">有些错误导致某些行无法被翻译</span>

你可能会遇到像这样的错误 :

```python
2024-01-30 14:55:19 Error in line:1320 D:\Download\Nova-Pasta\SunshineLoveCH2-1.01-pc\game\tl\Portugues/10_week10_00.rpy
"It’s [s_name]. And [y_name]."
It’s [0] . And [1] . Error
"É [0] . E 1] ."
```

这取决于翻译的结果，为了跳过翻译特殊符号像  '[]' '{}' '<>'  , 这个工具将用按顺序的数字替换特殊字符
举个例子:
"It’s [s_name]. And [y_name]."
将会被替换为
"It’s [0] . And [1] ."

通常来说，这种格式将不会被翻译且会保留  '[0]' 和  '[1]' ，并且这个工具将会根据这个有序数字还原原本的内容

然而，有时这种格式会在翻译后被破坏，正如前面提到的： "É [0] . E 1] ."
你会发现  '['  丢了，所以本工具无法还原原本的内容，因此这行文本不会被翻译
你可能需要手动修正这些行
幸运的是这种情况很少发生，你不会花费很多时间在修正这些行上

### 杀毒软件报毒

~~这个软件是用 pyinstaller 打包的，且因为有文件操作(打开 读 写) ，因此可能会有误检测~~

~~如果你对此表示担忧，你可以自己下载源码并运行~~

Pyinstaller 构建的版本很容易被误检测为病毒

如果你对此表示担忧  , 可以尝试 Nuitka 构建的版本(Nuitka.Build 或 RenpyTranslatorInstaller)

| 正式包                                    | 解释                | 优点                               | 缺点                       |
| ----------------------------------------- | ------------------- | ---------------------------------- | -------------------------- |
| RenpyTranslator-Win.Pyinstaller.Build.zip | 由 Pyinstaller 构建 | 可执行文件只有一个更轻量           | 可能会被误检测为 **病毒**  |
| RenpyTranslator-Win.Nuitka.Build.zip      | 由 Nuitka 构建      | 不会被绝大多数杀毒软件误检测为病毒 | 可执行文件包含很多额外的库 |
| RenpyTranslatorInstaller.exe              | Nuitka 版本的安装包 | 更易于安装使用                     | 需要安装                   |

### 运行翻译后的游戏报错

当你翻译完游戏运行后可以会遇到类似下面的报错

![error_after_translation](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/error_after_translation.png)

![error_after_translation_source](https://github.com/anonymousException/renpy-translator/blob/main/docs/img/error_after_translation_source.png)

不难发现在翻译过后 "[[XXXX]" 被翻译成了"[ [XXXX]" , 多了个空格  (你遇到的可能是其它形式的错误，但重点在于在翻译后**特殊符号的结构被破坏**了)

这个结果是翻译引擎翻译导致的 , 有时翻译引擎对特殊符号像 '[]' '<>' ... **不太友好** 特别是当特殊符号叠加使用时

但仍然有个好消息 , 通常这种情况不会很频繁发生，你只需要手动处理这些错误的句子 (对于我在上面提到的这个案例 , 只需要删除多余的空格即可)

### 有些句子在翻译过后好像没生效

#### tooltip

对于在 **tooltip** 里的特殊文本，明明翻译了却没生效

原始的代码看起来像这样 :

```python
tooltip "this is a tooltip"
```

参考来自 https://f95zone.to/threads/translation-of-text-in-screen.90781/ 的教程

只需要打开 rpy 文件 (随便一个在 tl 文件夹底下的或你可以自己创一个) 并添加以下代码

```python
#如果是自己创建的话，需要补上下面这行去掉 # , tl_name 填 tl 目录下的文件夹名称如 schinese
#translate tl_name strings:
    old "[tooltip]"
    new "[tooltip!t]"
```

#### notify

对于在 **notify** 里的特殊文本 ，明明翻译了却没生效

你需要定位没被翻译的句子在原本代码里的位置 (不是在翻译的 tl 文件夹下)

你将会找到看起来像这样的原始代码 :

```python
show screen notify(_("Find old Man Gibson"), None)
```

------

替换为

```python
show screen notify(__("Find old Man Gibson"), None)
```

操作只是在notify( 后添加 '_'

很简单对吧? 然后翻译就能生效了

#### 其它

可能会有其它情况，有些句子在翻译后仍然没生效

这取决于原始的代码，抽取可能不能完全覆盖如果原始代码写得不是那么得对翻译友好

为了避免多余的无效抽取，本工具的抽取功能不会抽取满足以下格式的句子：

句子长度小于 8 (空格和特殊符号长度被记为 0)

举个例子 :

```
"I know [special symbol]"
```

实际有效的内容是：

```
Iknow
```

长度只有 5 , 所以它不会被本工具的抽取功能抽取

------

除此之外，在 [ConditionSwitch()](https://www.renpy.org/doc/html/displayables.html#ConditionSwitch)  里的内容同样不会被翻译， 因为分支选择的代码可能会被包含在里面

### 在抽取后生成了 0KB 的文件

这是正常的，因为目标文件没有可抽取的内容

别删除 0 KB 的文件，它被用来占位

如果 0 KB 文件不存在可能会导致错误产生

### 在抽取后生成的奇怪内容

在抽取后你会看到类似下面的内容

```python
old "old:1709016761.706834_0.8853030081254853"
new "new:1709016761.706834_0.8853030081254853"
```

这是一个不重复的时间戳用来标记你抽取的时间，格式是 时间戳_随机数(随机数是为了确保生成的内容不重复否则会引起错误)

你可以转换在 '_' 前的部分 (本例是1709016761.706834) 为可读的时间通过 https://www.epochconverter.com/ 或其它能转换时间戳的网站

### OpenAI

你可以在 : [rate-limits](https://platform.openai.com/account/rate-limits)  查看速率限制并设置一个合理的限制

如果是 OpenAI 新用户，每分钟请求数最多 3 个，基本无法使用

默认设置就是针对这种情况 ，如果你不在意多花点时间 ,你可以使用默认设置

对于更高权限的用户 , 推荐提高配置 推荐配置如下

| 参数                       | 推荐                                                         |
| -------------------------- | ------------------------------------------------------------ |
| RPM(requests per minute)   | 250                                                          |
| RPS(requests per second)   | 10                                                           |
| TPM(requests token limits) | [rate-limits](https://platform.openai.com/account/rate-limits) |
| model                      | gpt-3.5-turbo \| gpt-4 (更智能但更贵)                        |

####  [有些错误导致某些行无法被翻译](#jump_error_translate_special_symbols)

OpenAI 似乎对像 '{}' '[]' 的特殊符号不太友好 , 你可能会遇到前面提到的问题 : [有些错误导致某些行无法被翻译](#jump_error_translate_special_symbols)

你可以用谷歌翻译重新翻译这些错误的行 (已经被翻译过的行将会被**自动跳过**，只需要重新翻译之前翻译过的整个目录或文件即可)

(谷歌翻译会对这些特殊符号更友好但仍然可能留下一点点错误) 

最后你需要手动处理剩下的一点点错误

除此之外如果你在使用 openai 时遇到 traceback 错误 ， 尝试禁用 Multi-Translate 选项，并重新翻译 (更稳定但会慢一些)

#### JSONDecodeError

你可能遇到如下错误:

```python
2024-02-22 11:18:28	Traceback (most recent call last):
  File "openai_translate.py", line 180, in translate_limit
  File "json\__init__.py", line 346, in loads
  File "json\decoder.py", line 337, in decode
  File "json\decoder.py", line 353, in raw_decode
json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 1613 (char 1612)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "openai_translate.py", line 187, in translate_limit
Exception: Unterminated string starting at: line 1 column 1613 (char 1612)
```

这是由于 openai 返回了错误的数据格式 , 幸运的是这并不会频繁发生并且只会导致一个文件部分内容未被成功翻译，你可以用其它翻译引擎像谷歌翻译来重新翻译这些未被翻译的行

#### 不匹配的翻译结果

你可能会遇到如下报错：

```python
2024-02-23 10:19:34 translated result can not match the untranslated contents
```

原因在于 open-ai 可能会偶然把多个翻译结果混合成一个 ,  例如 :

```
#untranslated
["Hello","Good"]
#translated
["こんにちは,良い"]
```

这会导致翻译结果的不匹配 ， 因此这部分内容的翻译不会生效 , 你可能需要用其它翻译引擎翻译这些未翻译的内容

#### ConnectError

你可能会遇到如下报错：

```python
2024-02-23 10:19:34	Another non-200-range status code was received:400 <Response [400 Bad Request]>
2024-02-23 10:19:34	Error code: 400 - {'error': {'message': 'Connection error (request id: 20240223101928248984704uoEfBgvh)', 'type': '', 'param': '', 'code': 'connection_error'}}
2024-02-23 10:19:34	['untranslated1','untranslated2','....']
```

这取决于你的网络环境，重新翻译可能就可以了

