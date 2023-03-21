import win32gui
import win32ui
import win32api
import cv2
import time
import win32con
from PIL import Image
from PIL import ImageDraw
from ctypes import windll
import numpy as np
import random

DEBUG = True

def calcCoords2(oldCoords):

    oldWndInfo = {
        "left" : 1598, 
        "top" : 825, 
        "width" : 322, 
        "height" : 215
    }
    hwnd = win32gui.FindWindow(None, 'LDPlayer')

    newCoords = []
    randNum = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        if(DEBUG) : print(f"hwnd = {left}, {top}, {w}, {h}")

        for oldCoord in oldCoords:
            x_ratio = (oldCoord[0] - oldWndInfo["left"]) / oldWndInfo["width"]
            y_ratio = (oldCoord[1] - oldWndInfo["top"]) / oldWndInfo["height"]

            # newCoords.append((round(left + w*x_ratio), round(top + h*y_ratio)))
            newCoords.append((round(w*x_ratio), round(h*y_ratio)))
        
        x_ratio = (1620 - oldWndInfo["left"]) / oldWndInfo["width"]
        y_ratio = (960 - oldWndInfo["top"]) / oldWndInfo["height"]
        # randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
        randNum.append((round(w*x_ratio), round(h*y_ratio)))

        x_ratio = (1660 - oldWndInfo["left"]) / oldWndInfo["width"]
        y_ratio = (963 - oldWndInfo["top"]) / oldWndInfo["height"]
        # randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
        randNum.append((round(w*x_ratio), round(h*y_ratio)))
    return newCoords, randNum

def click(x, y):
    print(f"click ({x}, {y})")
    hWnd = win32gui.FindWindow(None, hwndname)
    lParam = win32api.MAKELONG(x, y)

    hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)


                
if __name__ == "__main__":

    # 좌표 리스트
    coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
            (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
            (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
            (1901, 952), (1819, 924), (1777, 997), (1899, 872),(1905, 985),
            (1905,933), (1878, 870),] 
    coords, randNum = calcCoords2(coords)

    hwndname = 'LDPlayer'
    hwnd = win32gui.FindWindow(None, hwndname)

    if hwnd >= 1:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        draw = ImageDraw.Draw(im)
        for idx, pos in enumerate(coords):
            draw.text(pos, f"{idx}", (255,0,0))
        draw.rectangle((randNum[0][0], randNum[0][1], randNum[1][0], randNum[1][1]), outline=(255,0,0), width=2)
        im.show()


    
    
