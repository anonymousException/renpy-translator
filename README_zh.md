<div align=center><img src = "https://www.renpy.org/static/index-logo.png"></div>

# <div align=center>Renpy 翻译器</div>

<div align=center>一款免费开源的ren'py 翻译工具</div>

<div align=center>只支持 python 3.8 因为 dl-translate</div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/assets/157234942/5b77a190-991e-420b-9d18-093db64ebdaa"></div>

------

## 下载

你可以通过 [[https://github.com/anonymousException/renpy-translator/releases/latest](https://github.com/anonymousException/renpy-translator/releases/tag/v2.0.1-alpha)](https://github.com/anonymousException/renpy-translator/releases/tag/v2.0.1-alpha) 下载 AI 版本

## 其它文档

### 不带 AI 版

如果你想要一个轻量工具或者更具体的功能说明，可以前往 :

https://github.com/anonymousException/renpy-translator/blob/main/README_zh.md

------

## AI 特性

支持离线 AI 翻译基于 [dl-translate](https://github.com/xhluca/dl-translate)

需要下载相关的 AI 模型 : (不需要全部下载 , 选一个你喜欢的，默认推荐是 m2m100)

- m2m100：https://huggingface.co/facebook/m2m100_418M/tree/main
- mbart50：https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt/tree/main
- nllb200：https://huggingface.co/facebook/nllb-200-distilled-600M/tree/main

优点:

- 离线: 支持离线翻译只要 AI 模型已经下载好了
- 精确 : 可能会比谷歌更精确

缺点:

- 笨重: 为了跑 AI 模型工具变得很大并且会消耗电脑性能去跑 ， Gpu 模式只在 cuda (NVDIA 才有) 下能生效
- 慢:  比谷歌慢了很多，因为需要你本地机器去运转
- 呆板: 不支持特殊符号像 "{}" "[]" and "<>" , 你可能需要再用谷歌翻译一遍
