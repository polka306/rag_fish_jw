import pyautogui
import time
import os
import win32gui

#pyautogui.mouseInfo()

ldplayerName ="LDPlayer"

oldCoords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
          (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
          (1878, 870), (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
          (1901, 952), (1819, 924), (1777, 997), (1899, 872),]

oldWndInfo = {
    "left" : 1599, 
    "top" : 819, 
    "width" : 322, 
    "height" : 215
 } #left, top, width, height, 창 우측 하단 최소화 했을때 윈도우 정보


def calcCoords(oldCoords):
    global ldplayerName, oldWndInfo
    hwnd = win32gui.FindWindow(None, ldplayerName)

    newCoords = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        for oldCoord in oldCoords:
            x_ratio = (oldCoord[0] - oldWndInfo["left"]) / oldWndInfo["width"]
            y_ratio = (oldCoord[1] - oldWndInfo["top"]) / oldWndInfo["height"]

            newCoords.append((left + w*x_ratio, top + h*y_ratio))

    return newCoords

while True:

# 좌표 리스트
    coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
          (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
          (1878, 870), (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
          (1901, 952), (1819, 924), (1777, 997), (1899, 872),]    
          
       
# 좌표 순회
    for x, y in coords:
    # 좌표의 RGB값 가져오기
        r, g, b = pyautogui.pixel(x, y)

    # RGB값이 (255, 0, 0)인 경우 클릭        
        if (r, g, b) == (231,145,101):
            pyautogui.click(x, y)
            print("일퀘 클릭")  
            time.sleep(0.1)           
            break
        
        elif (r, g, b) == (125,155,226):
            pyautogui.click(x, y)
            print("일퀘 완료 건네기 좌표")
            time.sleep(0.1)
            break

        elif (r, g, b) == (119, 88, 118):
            pyautogui.click(x, y)
            print("스킵 화살용 좌표")
            time.sleep(0.1)
            break

        elif (r, g, b) == (150, 226, 103):
            pyautogui.click(x, y)
            print("스킵 아래 녹색 좌표")
            time.sleep(0.1)
            break

        elif (r, g, b) == (255,248,230):
            pyautogui.click(x, y)
            print("황금 테두리 하얀손가락")
            time.sleep(0.1)
            break

        elif (r, g, b) == (206,240,156):
            pyautogui.click(x, y)
            print("문답 지문 녹색1(위)+파란2 좌표")
            time.sleep(0.1)
            break
        elif (r, g, b) == (125,153,227):
            pyautogui.click(x, y)
            print("재료 건네기 좌표")
            time.sleep(0.1)
            break

        elif (r, g, b) == (205,232,164):
            pyautogui.click(x, y)
            print("문답 지문 녹색 좌표(1지문)")
            time.sleep(0.1)
            break

        elif (r, g, b) == (229,229,237):
            pyautogui.click(x, y)
            print("문답 지문 하얀색 좌표")
            time.sleep(0.1)
            break

        elif (r, g, b) == (231,229,232):
            pyautogui.click(x, y)
            print("일퀘 우측 나가기 버튼")
            time.sleep(0.1)
            break
    
    else:
        # 좌표 순회가 완료되었을 때 실행되는 부분
        pyautogui.click(1650,960, interval=5)
        



           


         

        
