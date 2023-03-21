import win32gui
import win32ui
import win32api
import time
import win32con
from PIL import Image
from PIL import ImageDraw
from ctypes import windll
from easydict import EasyDict
import json

# import numpy as np
# import random

DEBUG = True

ldplayerName = 'LDPlayer'

class JsonConfigFileManager:
    """Json설정파일을 관리한다"""
    def __init__(self, file_path):
        self.values = EasyDict()
        if file_path:
            self.file_path = file_path # 파일경로 저장
            self.reload()

    def reload(self):
        """설정을 리셋하고 설정파일을 다시 로딩한다"""
        self.clear()
        if self.file_path:
            with open(self.file_path, 'r') as f:
                self.values.update(json.load(f))

    def clear(self):
        """설정을 리셋한다"""
        self.values.clear()
                
    def update(self, in_dict):
        """기존 설정에 새로운 설정을 업데이트한다(최대 3레벨까지만)"""
        for (k1, v1) in in_dict.items():
            if isinstance(v1, dict):
                for (k2, v2) in v1.items():
                    if isinstance(v2, dict):
                        for (k3, v3) in v2.items():
                            self.values[k1][k2][k3] = v3
                    else:
                        self.values[k1][k2] = v2
            else:
                self.values[k1] = v1     
            
    def export(self, save_file_name):
        """설정값을 json파일로 저장한다"""
        if save_file_name:
            with open(save_file_name, 'w') as f:
                json.dump(dict(self.values), f)

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

def calcCoordsRatio(oldCoords, oldWndInfo):

    hwnd = win32gui.FindWindow(None, 'LDPlayer')

    newCoords = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        if(DEBUG) : print(f"hwnd = {left}, {top}, {w}, {h}")

        for oldCoord in oldCoords:
            x_ratio = (oldCoord[0] - oldWndInfo["left"]) / oldWndInfo["width"]
            y_ratio = (oldCoord[1] - oldWndInfo["top"]) / oldWndInfo["height"]

            # newCoords.append((round(left + w*x_ratio), round(top + h*y_ratio)))
            newCoords.append((x_ratio, y_ratio))
        
        # x_ratio = (1620 - oldWndInfo["left"]) / oldWndInfo["width"]
        # y_ratio = (960 - oldWndInfo["top"]) / oldWndInfo["height"]
        # # randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
        # newCoords.append((x_ratio, y_ratio))

        # x_ratio = (1660 - oldWndInfo["left"]) / oldWndInfo["width"]
        # y_ratio = (963 - oldWndInfo["top"]) / oldWndInfo["height"]
        # # randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
        # newCoords.append((x_ratio, y_ratio))
    return newCoords

def calcCoordsFromConfig(config):
    global ldplayerName

    hwnd = win32gui.FindWindow(None, ldplayerName)

    newCoords = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        if(DEBUG) : print(f"hwnd = {left}, {top}, {w}, {h}")

        for name, ratio in config.values.quest.coords.items():
            # newCoords.append((round(left + w*ratio[0]), round(top + h*ratio[1])))
            newCoords.append((round(w*ratio[0]), round(h*ratio[1])))
            if(DEBUG) : print(f"{name} : {newCoords[-1]}")
        
        # x_ratio = (1620 - oldWndInfo["left"]) / oldWndInfo["width"]
        # y_ratio = (960 - oldWndInfo["top"]) / oldWndInfo["height"]
        # randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))

        # x_ratio = (1660 - oldWndInfo["left"]) / oldWndInfo["width"]
        # y_ratio = (963 - oldWndInfo["top"]) / oldWndInfo["height"]
        # randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
    return newCoords

def click(x, y):
    print(f"click ({x}, {y})")
    hWnd = win32gui.FindWindow(None, hwndname)
    lParam = win32api.MAKELONG(x, y)

    hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)


                
if __name__ == "__main__":

    conf = JsonConfigFileManager('./config.json')
    # 좌표 리스트
    # coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
    #         (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
    #         (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
    #         (1901, 952), (1819, 924), (1777, 997), (1899, 872),(1905, 985),
    #         (1905,933), (1878, 870),] 
    oldWndInfo = {
        "left" : 1471, 
        "top" : 865, 
        "width" : 322, 
        "height" : 215
    }
    coords = [(1754,1034)]
    coords = calcCoordsRatio(coords, oldWndInfo)

    conf.update({'fishing':{'coords':coords}})

    print(conf.values)

    conf.export('./config_new.json')

    # coords = calcCoordsFromConfig(conf)
    # randNum = [
    #     (coords[-2][0], coords[-2][1]),
    #     (coords[-1][0], coords[-1][1])
    # ]
    # coords.remove(randNum[0])
    # coords.remove(randNum[1])

    # hwndname = 'LDPlayer'
    # hwnd = win32gui.FindWindow(None, hwndname)

    # if hwnd >= 1:
    #     left, top, right, bot = win32gui.GetWindowRect(hwnd)
    #     w = right - left
    #     h = bot - top
    #     hwndDC = win32gui.GetWindowDC(hwnd)
    #     mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    #     saveDC = mfcDC.CreateCompatibleDC()

    #     saveBitMap = win32ui.CreateBitmap()
    #     saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    #     saveDC.SelectObject(saveBitMap)

    #     result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    #     bmpinfo = saveBitMap.GetInfo()
    #     bmpstr = saveBitMap.GetBitmapBits(True)
    #     im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    #     win32gui.DeleteObject(saveBitMap.GetHandle())
    #     saveDC.DeleteDC()
    #     mfcDC.DeleteDC()
    #     win32gui.ReleaseDC(hwnd, hwndDC)

    # if result == 1:
    #     draw = ImageDraw.Draw(im)
    #     for idx, pos in enumerate(coords):
    #         draw.text(pos, f"{idx}", (255,0,0))
    #     draw.rectangle((randNum[0][0], randNum[0][1], randNum[1][0], randNum[1][1]), outline=(255,0,0), width=2)
    #     im.show()


    
    
