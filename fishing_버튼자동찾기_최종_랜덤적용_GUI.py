import win32gui
import time
# import pyautogui
# import os
# import win32ui
import win32api
#import cv2
import win32con
# from PIL import Image
from PIL import ImageGrab
# from pynput import mouse
from ctypes import windll
#import numpy as np
import random
# import multiprocessing
import tkinter as tk
from tkinter import messagebox
import threading

hwndname ="LDPlayer"
hwnd = win32gui.FindWindow(None, 'LDPlayer')

fishing_button = [1,1]

if hwnd >=1:    
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right -left
    h = bot - top
    check_color_position_x = left + (w-40)*0.822
    check_color_position_y = top + (h-30)*0.67 + 30
    fishing_button = [check_color_position_x, check_color_position_y]

    print('l : %d, r : %d, t : %d, b : %d \n' %(left,right,top,bot))
    print('w : %d , h : %d' %(w,h))
    print("button x : %f, button y : %f" %(check_color_position_x, check_color_position_y))

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
#     im.save("test1.png")

#pyautogui.mouseInfo()

def click(x, y):
    print(f"click ({x}, {y})")

    #마우스에 자유를 부여?
    # hWnd = win32gui.FindWindow(None, hwndname)
    # lParam = win32api.MAKELONG(x, y)

    # hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
    # win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    # win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

    # 마우스의 자유가 없음
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    # time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

fishing_button_tu = (fishing_button[0], fishing_button[1])

plag = True

def run_button_clicked():
    plag = True
    while True:
        time.sleep(random.random()*0.5)
        if(plag):
            time.sleep(1)
            screen = ImageGrab.grab()
            rgb = screen.getpixel(fishing_button_tu)
            print("rgb :: " + rgb.__str__())
            if rgb[0] > 200 and rgb[1] > 200  and rgb[2] >200 :
                # pyautogui.click(fishing_button_tu)
                click(round(fishing_button_tu[0]) + random.randint(1, 5), round(fishing_button_tu[1])+random.randint(1, 10))
                print("click _ start")
                plag = False
        else:
            screen = ImageGrab.grab()
            rgb = screen.getpixel(fishing_button_tu)
            print("rgb :: " + rgb.__str__())
            if 100 < rgb[0] and 100 < rgb[1] and 150 > rgb[2] :
                # pyautogui.click(fishing_button_tu)
                click(round(fishing_button_tu[0]) + random.randint(1, 5), round(fishing_button_tu[1])+random.randint(1, 10))
                print("click _ catch")
                plag = True
        if stop_event.is_set():
            break

def exit_button_clicked():
    stop_event.set()
    root.destroy()
    
root = tk.Tk()
root.title("자동낚시")
root.geometry("200x100")

run_button = tk.Button(root, text="실행", command=lambda: threading.Thread(target=run_button_clicked).start())
run_button.pack(pady=10)
run_button.pack()

stop_event = threading.Event()
exit_button = tk.Button(root, text="종료", command=exit_button_clicked)
exit_button.pack(pady=10)
exit_button.pack()

root.mainloop()

"""
while True:
    time.sleep(random.random()*0.5)
    if(plag):
        time.sleep(1)
        screen = ImageGrab.grab()
        rgb = screen.getpixel(fishing_button_tu)
        print("rgb :: " + rgb.__str__())
        if rgb[0] > 200 and rgb[1] > 200  and rgb[2] >200 :
            # pyautogui.click(fishing_button_tu)
            click(round(fishing_button_tu[0]) + random.randint(1, 5), round(fishing_button_tu[1])+random.randint(1, 10))
            print("click _ start")
            plag = False
    else:
        screen = ImageGrab.grab()
        rgb = screen.getpixel(fishing_button_tu)
        print("rgb :: " + rgb.__str__())
        if 100 < rgb[0] and 100 < rgb[1] and 150 > rgb[2] :
            # pyautogui.click(fishing_button_tu)
            click(round(fishing_button_tu[0]) + random.randint(1, 5), round(fishing_button_tu[1])+random.randint(1, 10))
            print("click _ catch")
            plag = True
"""