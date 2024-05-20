from __future__ import print_function
import sys,ctypes
from time import sleep

WIDTH = 1440
HEIGHT = 1080
HZ = 165

# https://stackoverflow.com/questions/20838201/resize-display-resolution-using-python-with-cross-platform-support
class ScreenRes(object):
    @classmethod
    def set(cls, width=None, height=None, depth=32):
        '''
        Set the primary display to the specified mode
        '''
        if width and height:
            print('Setting resolution to {}x{}'.format(width, height, depth))
        else:
            print('Setting resolution to defaults')

        if sys.platform == 'win32':
            cls._win32_set(width, height, depth)

    @staticmethod
    def _win32_set(width=None, height=None, Hz=None, depth=32):
        '''
        Set the primary windows display to the specified mode
        '''
        # Gave up on ctypes, the struct is really complicated
        #user32.ChangeDisplaySettingsW(None, 0)
        import win32api
        from pywintypes import DEVMODEType
        if width and height and Hz:

            if not depth:
                depth = 32

            mode = win32api.EnumDisplaySettings()
            mode.PelsWidth = width
            mode.PelsHeight = height
            mode.BitsPerPel = depth
            mode.DisplayFrequency = Hz
            win32api.ChangeDisplaySettingsEx()

            win32api.ChangeDisplaySettings(mode, 0)
        else:
            win32api.ChangeDisplaySettings(None, 0)

    @staticmethod
    def _win32_set_default():
        '''
        Reset the primary windows display to the default mode
        '''
        # Interesting since it doesn't depend on pywin32
        import ctypes
        user32 = ctypes.windll.user32
        # set screen size
        user32.ChangeDisplaySettingsW(None, 0)
if __name__ == '__main__':
    # https://github.com/xyba1337/ValorantEZTS/blob/main/true_stretched.py
    # Search window
    window_handle = 0
    while window_handle == 0:
        window_handle = ctypes.windll.user32.FindWindowW(None, "VALORANT  ")
        print("Valorant not found")
        sleep(1)

    ScreenRes.set(WIDTH, HEIGHT, HZ)

    sleep(3)

    # Change window properties
    style = ctypes.windll.user32.GetWindowLongW(window_handle, ctypes.c_int(-16))
    style = style & ~0x00800000  # WS_DLGFRAME removal
    style = style & ~0x00040000  # WS_BORDER removal
    ctypes.windll.user32.SetWindowLongW(window_handle, ctypes.c_int(-16), style)

    # Maximize window
    ctypes.windll.user32.ShowWindow(window_handle, ctypes.c_int(3))  # SW_MAXIMIZE

    print("True stretched applied")

    if input("cancel ? (press c):") == "c":ScreenRes.set() # Set default res
