import pyautogui
import time
import os
import random
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image
from PIL import ImageDraw
from ctypes import windll
import tkinter as tk
import threading
import sys
from easydict import EasyDict
import json

DEBUG = False

VERSION = "230316"

ldplayerName ="LDPlayer"
#ldplayerName ="포샵"

stop_event = threading.Event()
puase_event = threading.Event()

######################## Functions ###############################

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

def calcCoords(oldCoords):
    global ldplayerName

    oldWndInfo = {
        "left" : 1471, 
        "top" : 865, 
        "width" : 322, 
        "height" : 215
    }

    hwnd = win32gui.FindWindow(None, ldplayerName)

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

            newCoords.append((round(left + w*x_ratio), round(top + h*y_ratio)))
    else:
        print("창을 찾을 수 없습니다.")
        return -1
        
    return newCoords

def calcCoordsFromConfig(config, key, relative=False):
    global ldplayerName

    hwnd = win32gui.FindWindow(None, ldplayerName)

    newCoords = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        if(DEBUG) : print(f"hwnd = {left}, {top}, {w}, {h}")

        for name, ratio in config.values[key].coords.items():
            if(relative):
                newCoords.append((round(w*ratio[0]), round(h*ratio[1])))
            else:
                newCoords.append((round(left + w*ratio[0]), round(top + h*ratio[1])))
            if(DEBUG) : print(f"{name} : {newCoords[-1]}")

    return newCoords

def getPixelWnd(x, y, size=1):
    pixels = []
    for i in range(x-size, x+size+1):
        for j in range(y-size, y+size+1):
            try:
                pixels.append(pyautogui.pixel(i, j))
            except:
                print("픽셀값을 얻을 수 없습니다.")
                return -1
    return pixels

def findColorinPixels(pixels, targetRGB, rgbVariance=(3, 3, 3)):
    for pixel in pixels:
        if (pixel[0] >= targetRGB[0]-rgbVariance[0] and pixel[0] <= targetRGB[0]+rgbVariance[0]) and \
           (pixel[1] >= targetRGB[1]-rgbVariance[1] and pixel[1] <= targetRGB[1]+rgbVariance[1]) and \
           (pixel[2] >= targetRGB[2]-rgbVariance[2] and pixel[2] <= targetRGB[2]+rgbVariance[2]) :
            return True
    return False

def jwClick(x, y, offset=(0, 0)):
    # pyautogui.click(x, y)
    x = x - offset[0]
    y = y - offset[1]
    global ldplayerName
    hwnd = win32gui.FindWindow(None, ldplayerName)
    if hwnd >=1:    
        if(DEBUG) : print(f"click {x}, {y}")
        pos = (x,y)
        cli_pos = win32gui.ScreenToClient(hwnd, pos)
        lParam = win32api.MAKELONG(cli_pos[0]-1, cli_pos[1]-34)
        hWnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

conf = JsonConfigFileManager('./config.json')

def fishing():
    global puase_event, stop_event, conf
    step = 1
    fail_count = 0 

    while True:

        # 좌표 리스트    
        coords = calcCoordsFromConfig(conf,'fishing')
        if coords == -1:
            continue

        x,y = coords[0]
        pixels = getPixelWnd(x, y, 1)
        if pixels == -1:
            continue
        
        if step==1 :
            if(findColorinPixels(pixels, (228,228,243))):
                time.sleep(random.uniform(0.5, 1))
                random_x = random.randint(0,20)
                random_y = random.randint(0,5)
                jwClick(x-random_x, y-random_y)
                step = 2
                fail_count = 0
                time.sleep(random.uniform(0.5, 1))
                print("낚시 시작")
            else:
                fail_count += 1
        elif step==2:
            if(findColorinPixels(pixels, (229,222,243))):
                step = 3
                fail_count = 0
                print("낚시 중")
            else:
                fail_count += 1
        elif step == 3:
            if(findColorinPixels(pixels, (214,231,187 ))):
                time.sleep(random.uniform(0, 0.2))
                random_x = random.randint(0,20)
                random_y = random.randint(0,5)
                jwClick(x-random_x, y-random_y)
                step = 1
                fail_count = 0
                print("낚시 성공")
            else:
                fail_count += 1

        if fail_count > 50 :
            step = 1
            fail_count = 0
            print("에러발생함")

        if stop_event.is_set():
            break

def quest():
    global puase_event, stop_event, conf
    while True:
        coords = calcCoordsFromConfig(conf,'quest')
        randNum = [
            (coords[-2][0], coords[-2][1]),
            (coords[-1][0], coords[-1][1])
        ]
        coords.remove(randNum[0])
        coords.remove(randNum[1])
        
    # 좌표 순회
        for x, y in coords:
        # 좌표의 RGB값 가져오기
            # r, g, b = pyautogui.pixel(x, y)
            pixels = getPixelWnd(x, y, 1)

            # if(DEBUG): print(f"{coords.index((x,y))} ({x}, {y}) : {pixels}")

            x=random.randint(x, x+4)
            y=random.randint(y, y+4)

            e=random.randint(randNum[0][0], randNum[1][0])
            w=random.randint(randNum[0][1], randNum[1][1])

            p = random.uniform(4 , 6)

            if findColorinPixels(pixels, (231,145,101)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay) 
                jwClick(x, y)
                print("일퀘 클릭")          
                
            
            elif findColorinPixels(pixels, (125,155,226)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("일퀘 완료 건네기 좌표")
                

            elif findColorinPixels(pixels, (119, 88, 118)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("스킵 화살용 좌표")
                

            elif findColorinPixels(pixels, (150, 226, 103)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("스킵 아래 녹색 좌표")
                

            elif findColorinPixels(pixels, (255,248,230)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("황금 테두리 하얀손가락")
                

            elif findColorinPixels(pixels, (206, 231,165)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("문답 지문 녹색2")            
                

            elif findColorinPixels(pixels, (206,240,156)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("문답 지문 녹색1(위)+파란2 좌표")
                

            elif findColorinPixels(pixels, (212,237,176)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("문답 지문 녹색1(위)+파란3 좌표")
                

            elif findColorinPixels(pixels, (125,153,227)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("재료 건네기 좌표")
                

            elif findColorinPixels(pixels, (205,232,164)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("문답 지문 녹색 좌표(1지문)")
                

            elif findColorinPixels(pixels, (229,229,237), (1,1,1)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print(f"문답 지문 하얀색 좌표 = {x}, {y}")
                

            elif findColorinPixels(pixels, (231,229,232), (1,1,1)):
                delay = random.uniform(0.5, 1) 
                time.sleep(delay)
                jwClick(x, y)
                print("일퀘 우측 나가기 버튼")

        time.sleep(1)
        jwClick(e, w) # 좌측 일퀘 진행 부분 클릭
        time.sleep(p)
        
        if stop_event.is_set():
            break

# fishing_thread = threading.Thread(target=fishing)
# quest_thread = threading.Thread(target=quest)
# main_thread = fishing_thread
main_thread = threading.Thread(target=fishing)
pauseFlag = True
def start_button_clicked():
    global pauseFlag, start_button, main_thread
    if pauseFlag == True:
        if main_thread is None:
            selectMacro_clicked()
        stop_event.clear()
        main_thread.start()
        pauseFlag = False
        start_button['text'] = "■"
    else:
        stop_event.set()
        # puase_event.set()
        main_thread.join()
        main_thread = None
        pauseFlag = True
        start_button['text'] = "▶"

def exit_button_clicked():
    stop_event.set()
    main_thread.join()
    root.destroy()
    sys.exit(0)

def setWindowName(event):
    global ldplayerName
    ldplayerName = etWndName.get()

def selectMacro_clicked():
    global cbSelectMacro, main_thread, ldplayerName
    if cbSelectMacro.get() == '낚시':
        main_thread = threading.Thread(target=fishing)
    elif cbSelectMacro.get() == '일퀘':
        main_thread = threading.Thread(target=quest)

    ldplayerName = etWndName.get()

def checkPoint_clicked():
    conf = JsonConfigFileManager('./config.json')
    if cbSelectMacro.get() == '낚시':
        coords = calcCoordsFromConfig(conf, "fishing", True)
    elif cbSelectMacro.get() == '일퀘':
        coords = calcCoordsFromConfig(conf, "quest", True)

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
        if cbSelectMacro.get() == '일퀘':
            randNum = [
                (coords[-2][0], coords[-2][1]),
                (coords[-1][0], coords[-1][1])
            ]
            coords.remove(randNum[0])
            coords.remove(randNum[1])
            draw.rectangle((randNum[0][0], randNum[0][1], randNum[1][0], randNum[1][1]), outline=(255,0,0), width=2)

        for idx, pos in enumerate(coords):
            draw.text(pos, f"{idx}", (255,0,0))
        im.show()

if __name__ == '__main__':

    root = tk.Tk()
    root.title(f"BanPoLoga {VERSION}")
    root.geometry("300x100+200+200")
    # root.resizable(False, False)

    lbWndName=tk.Label(root, text="창 이름:", width=10)
    lbWndName.grid(row=0, column=0)

    etWndName = tk.Entry(root, width=15)
    etWndName.bind("<Return>", setWindowName)
    etWndName.grid(row=0, column=1)
    etWndName.insert(0, "LDPlayer")

    lbSelMacro=tk.Label(root, text="매크로 선택:", width=10)
    lbSelMacro.grid(row=1, column=0)

    macroList = [
        '낚시',
        '일퀘'
    ]

    cbSelectMacro=tk.ttk.Combobox(root, height=15,width=10, values=macroList)
    cbSelectMacro.grid(row=1, column=1)
    cbSelectMacro.set("낚시")

    btnSelectMacro = tk.Button(root, text="설정", command=selectMacro_clicked)
    btnSelectMacro.grid(row=1, column=2)

    btnCheckPoint = tk.Button(root, text="좌표확인", command=checkPoint_clicked)
    btnCheckPoint.grid(row=1, column=3)

    start_button = tk.Button(root, text="▶", command=start_button_clicked, width=15)
    start_button.grid(row=2, column=0)

    exit_button = tk.Button(root, text="종료", command=exit_button_clicked, width=15)
    exit_button.grid(row=3, column=0)

    puase_event.set()

    root.mainloop()