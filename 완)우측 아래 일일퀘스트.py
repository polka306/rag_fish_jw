import pyautogui
import time
import os
import random
import win32gui
import win32api
import win32con

DEBUG = True

ldplayerName ="LDPlayer"
# ldplayerName ="포샵"

oldWndInfo = {
    "left" : 1598, 
    "top" : 825, 
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
        
        x_ratio = (1620 - oldWndInfo["left"]) / oldWndInfo["width"]
        y_ratio = (960 - oldWndInfo["top"]) / oldWndInfo["height"]
        randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))

        x_ratio = (1660 - oldWndInfo["left"]) / oldWndInfo["width"]
        y_ratio = (963 - oldWndInfo["top"]) / oldWndInfo["height"]
        randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
    return newCoords, randNum

def getPixelWnd(x, y, size=1):
    pixels = []
    for i in range(x-size, x+size):
        for j in range(y-size, y+size):
            pixels.append(pyautogui.pixel(i, j))
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
    global ldplayerName
    y = y - 35
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
    # 좌표 리스트
    coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
            (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
             (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
            (1901, 952), (1819, 924), (1777, 997), (1899, 872),(1905, 985),
            (1905,933), (1878, 870),] 
    coords, randNum = calcCoords(coords)

    while True:
        
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
                
        
        # 좌표 순회가 완료되었을 때 실행되는 부분
        # pyautogui.click( e ,w , interval= p )
        # time.sleep(1)
        # pyautogui.click( e ,w , interval= p )
        time.sleep(1)
        jwClick(e, w)
        time.sleep(p)

        
if __name__ == '__main__':
    main()


           


         

        
