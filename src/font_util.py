import os
import win32gui
import win32con
import winreg


def get_font_path(font_name):
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts")
    for i in range(0, winreg.QueryInfoKey(key)[1]):
        value = winreg.EnumValue(key, i)
        if font_name in value[0]:
            return os.path.join(os.environ['SystemRoot'], 'Fonts', value[1])
    return None


def get_default_font_name():
    nonclient_metrics = win32gui.SystemParametersInfo(win32con.SPI_GETNONCLIENTMETRICS)
    font_name = nonclient_metrics['lfMessageFont'].lfFaceName
    return font_name


def get_default_font_path():
    return get_font_path(get_default_font_name())
