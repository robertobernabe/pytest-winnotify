from win32api import *
from win32gui import *
import win32con
import sys, os
import struct


class WinTrayIcon(object):
    MSG_INFO = NIIF_INFO
    MSG_ERROR = NIIF_ERROR
    MSG_WARNING = NIIF_WARNING

    def __init__(self, tooltip, iconFilePath=None):
        message_map = {win32con.WM_DESTROY: self.on_destroy}
        self.wc = WNDCLASS()  # Register the Window class.
        self.hinst = self.wc.hInstance = GetModuleHandle(None)
        self.wc.lpszClassName = "PythonTaskbar"
        self.wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        self.wc.hCursor = LoadCursor( 0, win32con.IDC_ARROW )
        self.wc.hbrBackground = win32con.COLOR_WINDOW
        self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
        self.classAtom = RegisterClass(self.wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(self.classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT,
                                 win32con.CW_USEDEFAULT, 0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)
        iconFilePath = os.path.abspath(iconFilePath)
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           self.hicon = LoadImage(self.hinst, iconFilePath, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            self.hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_INFO
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, tooltip)
        Shell_NotifyIcon(NIM_ADD, nid)

    def balloon_tip(self, title, message, icon=NIIF_INFO):
        flags = NIF_ICON | NIF_MESSAGE | NIF_INFO
        #define the icon properties (see http://msdn.microsoft.com/library/default.asp?url=/library/en-us/shellcc/platform/shell/reference/structures/notifyicondata.asp)
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, title, message, 10, title, icon)
        Shell_NotifyIcon(NIM_MODIFY, nid)

    def close(self):
        DestroyWindow(self.hwnd)
        UnregisterClass(self.classAtom, self.hinst)

    def on_destroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.



