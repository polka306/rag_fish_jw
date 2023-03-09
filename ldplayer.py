import win32gui
import win32ui
import win32api
import cv2
import time
import win32con
from PIL import Image
from PIL import ImageGrab
from ctypes import windll
import numpy as np
import random


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
    im.save("test1.png")

def click(x, y):
    print(f"click ({x}, {y})")
    hWnd = win32gui.FindWindow(None, hwndname)
    lParam = win32api.MAKELONG(x, y)

    hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

# def Capture():
#     global hwnd
#     x, y, w, h = win32gui.GetWindowRect(hwnd)
#     cap = np.array(ImageGrab.grab(bbox=(x, y, w, h)))
#     return cap

def img_click(img, thy=0.8):
    cap = np.array(ImageGrab.grab())
    src = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    temp = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    ih, iw = temp.shape

    res = cv2.matchTemplate(src, temp, cv2.TM_CCOEFF_NORMED)
    Min_val, Max_val, Min_loc, Max_loc = cv2.minMaxLoc(res)

    x, y = Max_loc
    x += round((iw / 2))
    y += round((ih / 2))
    y -= 25
    if Max_val >= thy:
        click(x, y)
        time.sleep(random.uniform(0.04, 0.05))
        print("click!!")
        return 0
    else:
        return 1
    
def imsrc(img, thy=0.05):

    global hwnd
    x, y, w, h = win32gui.GetWindowRect(hwnd)
    cap = np.array(ImageGrab.grab(bbox=(x,y,w,h)))
    src = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    temp = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    
    # res = cv2.matchTemplate(src, temp, cv2.TM_CCOEFF_NORMED)
    res = cv2.matchTemplate(src, temp, cv2.TM_SQDIFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(f"{img} = {min_val} , th = {thy}")

    if min_val <= thy:
        print("찾았다!")
        return 0
    else:
        print("못찾음!")
        return 1
    
def fish():
    if imsrc("fish1.png") == 0:
        img_click("fish1.png")
        timeout = time.time() + 10000
        while True:
            if imsrc("fish2.png") == 0:
                time.sleep(0.05)

                if time.time() >= timeout:
                    break

                if(imsrc("fish4.png", 0.89)) == 0:
                    img_click("fish4.png")
                    return 0
                
if __name__ == "__main__":
    while True:
        fish()
    
