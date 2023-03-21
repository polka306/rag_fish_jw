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

            newCoords.append((x_ratio, y_ratio))
        
    return newCoords

def click(x, y):
    print(f"click ({x}, {y})")
    hWnd = win32gui.FindWindow(None, ldplayerName)
    lParam = win32api.MAKELONG(x, y)

    hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)


                
if __name__ == "__main__":

    conf = JsonConfigFileManager('./config.json')

    coords = calcCoordsRatio(conf.values.quest.oldCoords, conf.values.quest.oldWndSize)
    conf.update({'quest':{'coords':coords}})

    coords = calcCoordsRatio(conf.values.fishing.oldCoords, conf.values.fishing.oldWndSize)
    conf.update({'fishing':{'coords':coords}})

    print(conf.values)

    conf.export('./config_new.json')


    
    
