import pyautogui
import time
import win32gui

DEBUG = True

# ldplayerName ="LDPlayer"
ldplayerName ="포샵"

oldWndInfo = {
    "left" : 1598, 
    "top" : 825, 
    "width" : 322, 
    "height" : 215
 }

pyautogui.mouseInfo()

######################## Functions ###############################

def calcCoords(oldCoords, oldBtnsPos):
    global ldplayerName, oldWndInfo
    hwnd = win32gui.FindWindow(None, ldplayerName)

    newCoords = []
    btnPos = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        if(DEBUG) : print(f"hwnd = {left}, {top}, {w}, {h}")

        for oldCoord in oldCoords:
            listInnerCoord = []
            for c in oldCoord:
                x_ratio = (c[0] - oldWndInfo["left"]) / oldWndInfo["width"]
                y_ratio = (c[1] - oldWndInfo["top"]) / oldWndInfo["height"]

                listInnerCoord.append((round(left + w*x_ratio), round(top + h*y_ratio)))
            newCoords.append(listInnerCoord)

        for oldBtn in oldBtnsPos:
            x_ratio = (oldBtn[0] - oldWndInfo["left"]) / oldWndInfo["width"]
            y_ratio = (oldBtn[1] - oldWndInfo["top"]) / oldWndInfo["height"]
            btnPos.append((round(left + w*x_ratio), round(top + h*y_ratio)))
                
    return newCoords, btnPos

def getPixelWnd(x, y, size=1):    
    pixels = []
    for i in range(x-size, x+size):
        for j in range(y-size, y+size):
            pixels.append(pyautogui.pixel(i, j))
    if(DEBUG) : print(f"getPixelWnd({x}, {y}): {pixels} ")
    return pixels

def findColorinPixels(pixels, targetRGB, rgbVariance=(3, 3, 3)):
    for pixel in pixels:
        if (pixel[0] > targetRGB[0]-rgbVariance[0] and pixel[0] <= targetRGB[0]+rgbVariance[0]) and \
           (pixel[1] > targetRGB[1]-rgbVariance[1] and pixel[1] <= targetRGB[1]+rgbVariance[1]) and \
           (pixel[2] > targetRGB[2]-rgbVariance[2] and pixel[2] <= targetRGB[2]+rgbVariance[2]) :
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


coordinates_list = [
    [(1629, 949), (1617, 909), (1795, 976)],
    [(1675, 949), (1665, 909), (1722, 949)],
    [(1722, 949), (1709, 909), (1767, 949)],
    [(1767, 949), (1757, 909), (1814, 949)],
    [(1814, 949), (1802, 909), (1629, 1012)],
    [(1629, 1012), (1619, 974), (1675, 1012)],
    [(1675, 1012), (1665, 974), (1722, 1012)],
    [(1722, 1012), (1709, 974), (1784, 879)]]

listBtnPos = [
    (1909, 894), # 시작좌표
    (1909, 894), # 길드 버튼 
    (1890, 1003), # 제출 버튼
    (1791, 902), # Get 버튼
    (1837, 916), # 추천 버튼
    (1889,882), 
    (1742, 981), 
    (1807, 959), 
    (1842, 959), 
    (1842, 976), 
    (1740, 1009),
    (1897, 872),
    (1797,976),
    (1834, 957),
    (1735, 886), 
    (1687, 934)
]

coordinates_list, BtnPos = calcCoords(coordinates_list, listBtnPos)

while True:
    # 시작 좌표의 RGB 값 확인
    if findColorinPixels(getPixelWnd(BtnPos[0][0], BtnPos[0][1], 0), (48,48,77), (1,1,1)):
        for coords in coordinates_list:
            pyautogui.click(coords[0][0],coords[0][1]) # 변수a 좌표 클릭
            pyautogui.sleep(1)
            print('길드 재료')

            # rgb_guild = pyautogui.pixel(1909, 894) # 길드 버튼 RGB 값을 가져옴
            if not findColorinPixels(getPixelWnd(BtnPos[1][0], BtnPos[1][1], 0), (48,48,77), (1,1,1)): # 길드 버튼 RGB가 맞지 않으면 다음 좌표로 이동
                print('길드 버튼 RGB가 맞지 않습니다.')
                continue
            else:
                # pyautogui.click(1890, 1003) 
                jwClick(BtnPos[2][0], BtnPos[2][1])
                pyautogui.sleep(1)
                print('제출')

                # rgb1 = pyautogui.pixel(1890, 1003)
                if findColorinPixels(getPixelWnd(BtnPos[2][0], BtnPos[2][1]), (120, 170, 87), (1,1,1)):
                    # pyautogui.click(coords[1][0], coords[1][1]) # 변수b 좌표 클릭
                    jwClick(coords[1][0], coords[1][1])
                    pyautogui.sleep(1)
                    print('아이템 클릭')

                    # pyautogui.click(1791, 902, interval=1) # Get 버튼
                    jwClick(BtnPos[3][0], BtnPos[3][1])
                    pyautogui.sleep(1)
                    print('Get 버튼 클릭')

                    # pyautogui.click(x=1837, y=916, interval=1) # 추천 버튼(상점이동)
                    jwClick(BtnPos[4][0], BtnPos[4][1])
                    print('상점으로 이동')
                    pyautogui.sleep(20)
            
                    # rgb2 = pyautogui.pixel(1889,882)             
                    if findColorinPixels(getPixelWnd(BtnPos[5][0], BtnPos[5][1]), (125, 96 ,181), (1,1,1)):
                        # pyautogui.click(x=1742, y=981, interval=1)
                        # pyautogui.click(x=1807, y=959, interval=1)
                        # pyautogui.click(x=1842, y=959, interval=1)
                        # pyautogui.click(x=1842, y=976, interval=1)
                        # pyautogui.click(x=1740, y=1009, interval=1)
                        # pyautogui.click(x=1897, y=872, interval=1)
                        jwClick(BtnPos[6][0], BtnPos[6][1])
                        jwClick(BtnPos[7][0], BtnPos[7][1])
                        jwClick(BtnPos[8][0], BtnPos[8][1])
                        jwClick(BtnPos[9][0], BtnPos[9][1])
                        jwClick(BtnPos[10][0], BtnPos[10][1])
                        jwClick(BtnPos[11][0], BtnPos[11][1])
                        print('아이템 구매완료')
                        pyautogui.sleep(1)
                                    
                    else:                  
                        print("아이템 구매 완료 후 재확인")                   
                
                else:
                    # RGB 값이 일치하지 않으면 다음 좌표 클릭
                    jwClick(coords[2][0], coords[2][1]) #1~8번까지 변수좌표 변수c
                    print('다음 좌표로 넘어가') 
                    pyautogui.sleep(1) 

                    # pyautogui.click(1797,976) 
                    jwClick(BtnPos[12][0], BtnPos[12][1])
                    pyautogui.sleep(1)    
                    print('수정확인') 

 
    else:        
            # rgb3 = pyautogui.pixel(1834, 957)
            if findColorinPixels(getPixelWnd(BtnPos[13][0], BtnPos[13][1]), (107, 90, 129), (1,1,1)):
                # pyautogui.click(1834, 957, interval=1)
                jwClick(BtnPos[13][0], BtnPos[13][1])
                time.sleep(1)
                print('길드버튼')

                # for pos in [ (1735, 886), (1687, 934)]:
                #     pyautogui.click(pos, interval=1)
                jwClick(BtnPos[14][0], BtnPos[14][1])
                time.sleep(1)
                print('길드 공헌')
                jwClick(BtnPos[15][0], BtnPos[15][1])
                time.sleep(1)
                print('길드 공헌')




                    