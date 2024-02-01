
<div align=center><img src = "https://www.renpy.org/static/index-logo.png"></div>

# <div align=center>Renpy Translator</div>

<div align=center>A free and open-source translator for ren'py</div>

<div align=center>Only supported in Python 3.8 due to dl-translate</div>

------

<div align=center><img src = "https://github.com/anonymousException/renpy-translator/assets/157234942/5b77a190-991e-420b-9d18-093db64ebdaa"></div>

------

## Download

You can download from [https://github.com/anonymousException/renpy-translator/releases/tag/v2.0.4-alpha](https://github.com/anonymousException/renpy-translator/releases/tag/v2.0.4-alpha)

## Another Docs

### No-AI Version

If you need a light tool or detail function introduction , you can refer to :

https://github.com/anonymousException/renpy-translator

### Chinese

<div align=center>中文版 README 在 <a href = 'https://github.com/anonymousException/renpy-translator/tree/feature/ai-translate/README_zh.md'>这里</a> </div>

## AI Feature

Support offline ai-translation based on [dl-translate](https://github.com/xhluca/dl-translate)

Need to download the relative ai-models:(need not to download all of them , choose one you prefer , the default recommendation is m2m100)

- m2m100：https://huggingface.co/facebook/m2m100_418M/tree/main
- mbart50：https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt/tree/main
- nllb200：https://huggingface.co/facebook/nllb-200-distilled-600M/tree/main

Advantage:

- offine : support offline translation only if the ai-model already downloaded
- accuracy : may be more accurate than google

Disadvantage:

- Heavy : the tool becomes very large to run ai model and will consume computer performance to run. Gpu mode only supported under cuda (NVIDIA only)
- Slow : slower than google because the speed depends on your local-machine
- Stiff : not support special symbols like "{}" "[]" and "<>" , you may need to re-translate it with google translation mode
