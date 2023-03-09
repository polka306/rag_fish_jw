import pyautogui
import time
import os
from PIL import ImageGrab

import cv2

#pyautogui.mouseInfo()



start_ok_pos = (1615,850)
start_ok_rgb = (255,255,255)

end_ok_pos = (1620,787)
end_ok_rgb = (219,231,195)

plag = True

while True:

    if(plag):
        time.sleep(1)
        screen = ImageGrab.grab()
        rgb = screen.getpixel(start_ok_pos)
        print("rgb :: " + rgb.__str__() + ",    start_ok_rgb :: " + start_ok_rgb.__str__())
        if rgb == start_ok_rgb:
            pyautogui.click(start_ok_pos)
            plag = False
    else:
        time.sleep(1)
        screen = ImageGrab.grab()
        rgb = screen.getpixel(end_ok_pos)
        print("rgb :: " + rgb.__str__() + ",    end_ok_rgb :: " + end_ok_rgb.__str__())
        if rgb == end_ok_rgb:
            pyautogui.click(end_ok_pos)
            plag = True





