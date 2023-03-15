import pyautogui
import time
import os
import random
import win32gui
import win32con
import win32api
import tkinter as tk
import threading
import sys

DEBUG = False

ldplayerName ="LDPlayer"
#ldplayerName ="포샵"

stop_event = threading.Event()
puase_event = threading.Event()

oldWndInfo = {
    "left" : 1471, 
    "top" : 865, 
    "width" : 322, 
    "height" : 215
 }

######################## Functions ###############################

def calcCoords(oldCoords):
    global ldplayerName, oldWndInfo
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

def jwClick(x, y):
    # pyautogui.click(x, y)
    y = y - 35
    global ldplayerName
    hwnd = win32gui.FindWindow(None, ldplayerName)
    if hwnd >=1:    
        if(DEBUG) : print(f"click {x}, {y}")
        pos = (x,y)
        cli_pos = win32gui.ScreenToClient(hwnd, pos)
        lParam = win32api.MAKELONG(cli_pos[0], cli_pos[1])
        hWnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)


def main():
    global puase_event, stop_event
    step = 1
    fail_count = 0 

    while True:

        if puase_event.is_set():
            continue

        # 좌표 리스트    
        coords = [(1754,1034)]
        coords = calcCoords(coords)
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

pauseFlag = True
def start_button_clicked():
    global pauseFlag, run_button
    if pauseFlag == True:
        puase_event.clear()
        pauseFlag = False
        run_button['text'] = "■"
    else:
        puase_event.set()
        pauseFlag = True
        run_button['text'] = "▶"

def exit_button_clicked():
    stop_event.set()
    root.destroy()
    sys.exit(0)

def setWindowName(event):
    global ldplayerName
    ldplayerName = etWndName.get()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("자동낚시")
    root.geometry("300x100+200+200")
    root.resizable(False, False)

    lbWndName=tk.Label(root, text="창 이름:", width=10)
    lbWndName.grid(row=0, column=0)

    etWndName = tk.Entry(root, width=20)
    etWndName.bind("<Return>", setWindowName)
    etWndName.grid(row=0, column=1)
    etWndName.insert(0, "LDPlayer") 

    run_button = tk.Button(root, text="▶", command=start_button_clicked, width=15)
    run_button.grid(row=1, column=0)

    exit_button = tk.Button(root, text="종료", command=exit_button_clicked, width=15)
    exit_button.grid(row=1, column=1)

    puase_event.set()

    main_thread = threading.Thread(target=main)
    main_thread.start()    
    

    root.mainloop()