import pyautogui
import time
import random
import win32gui

#pyautogui.mouseInfo()

DEBUG = True

# ldplayerName ="LDPlayer"
ldplayerName ="포샵"

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
    pyautogui.click(x, y)
    # global ldplayerName
    # hwnd = win32gui.FindWindow(None, ldplayerName)
    # if hwnd >=1:    
    #     left, top, right, bot = win32gui.GetWindowRect(hwnd)
    #     if(DEBUG) : print(f"click pos = {x-left}, {y-top}")
    #     lParam = win32api.MAKELONG(x-left, y-top)
    #     win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    #     win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

coords_dict = {'제출(녹색)': (1900, 950), 
               '제출완료': (1872, 1012),
               '플뤄스버튼': (1746,982),                
               '제품클릭': (1809, 922), 
               '제품 겟버튼': (1791, 904),
               '상점으로': (1841, 917), 
               '제출완료': (1872, 1012),
               '지도 위 흰색':(1902,862),
               '획득경로':(1858,1015),
               '제품클릭': (1809, 922), 
               '추천경로':(1783,915),

               }


coords1 = (1812,945)    # 예시: 숫자2
coords2 = (1842,964)  # 예시: 숫자0
coords3 = (1845,981)  # 예시: 녹색버튼
coords4 = (1750,1012)   # 예시: 구매버튼
coords5 = (1899, 872)  # 예시: X 버튼)
coords6 = (1640, 960)    # 예시: (NPC 에게)

wait_time=5
start_coord = (1640, 960)
pyautogui.click(start_coord)

event1_disabled = False
delay = random.uniform(0.8, 1.1)

while True:
    for key, coords in coords_dict.items():
        if pyautogui.pixelMatchesColor(coords[0], coords[1], (219, 244, 178)):
            time.sleep(1)
            pyautogui.click(coords)
            print(f"제출(녹)Clicked {key}")

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (217,144,118)): 
            time.sleep(1)
            pyautogui.click(coords)
            print(f"획득경로Clicked {key}")

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (255,239,174)): 
            time.sleep(1)
            pyautogui.click(coords)
            print(f"추천경로Clicked {key}")    

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (128,153,227)): 
            time.sleep(0.9)
            pyautogui.click(coords)
            print(f"제출완료Clicked {key}") 
            
            time.sleep(wait_time)
            if not pyautogui.pixelMatchesColor(coords[0], coords[1], (128, 153, 227)):
                print(f"{wait_time}초간 반응이 없어 {start_coord}를 클릭합니다.")
            pyautogui.click(start_coord)

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (235, 239, 247)) and not event1_disabled:
            time.sleep(1)
            pyautogui.click(coords)
            print(f"제품 클릭 Clicked {key}")
            event1_disabled = True 
           
        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (194,194,206)):
            time.sleep(1)
            pyautogui.click(coords)
            print(f"제품 겟버튼 Clicked {key}")
                        
        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (228, 183, 123)):
            time.sleep(1)
            pyautogui.click(coords)
            print(f"상점으로 Clicked {key}")     

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (156,153,154)):
            time.sleep(1)
            pyautogui.click(coords)
            print(f"플뤄스버튼 {key}") 

            time.sleep(delay)
            pyautogui.click(coords1)
            print(coords1)

            time.sleep(delay)
            pyautogui.click(coords2)                
            print(coords2)

            time.sleep(delay)
            pyautogui.click(coords3)
            print(coords3)

            time.sleep(delay)
            pyautogui.click(coords4)
            print(coords4)

            time.sleep(delay)
            pyautogui.click(coords5)
            print(coords5)

            time.sleep(delay)
            pyautogui.click(coords6)
            print(coords6)
            
            event1_disabled = False 
               
 
              
            
   