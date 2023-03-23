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

VERSION = "230315"

ldplayerName ="LDPlayer"
#ldplayerName ="포샵"

stop_event = threading.Event()
puase_event = threading.Event()

######################## Functions ###############################

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

def calcCoords2(oldCoords):
    global ldplayerName

    oldWndInfo = {
        "left" : 1598, 
        "top" : 825, 
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
        
        x_ratio = (1620 - oldWndInfo["left"]) / oldWndInfo["width"]
        y_ratio = (960 - oldWndInfo["top"]) / oldWndInfo["height"]
        randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))

        x_ratio = (1660 - oldWndInfo["left"]) / oldWndInfo["width"]
        y_ratio = (963 - oldWndInfo["top"]) / oldWndInfo["height"]
        randNum.append((round(left + w*x_ratio), round(top + h*y_ratio)))
    return newCoords, randNum

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

def jwClick(x, y, offset=35):
    # pyautogui.click(x, y)
    y = y - offset
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


def fishing():
    global puase_event, stop_event
    step = 1
    fail_count = 0 

    while True:

        # if puase_event.is_set():
        #     continue

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

def quest():
    global puase_event, stop_event
    while True:
        # if puase_event.is_set():
        #     continue

        # 좌표 리스트
        coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
                (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
                (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
                (1901, 952), (1819, 924), (1777, 997), (1899, 872),(1905, 985),
                (1905,933), (1878, 870),] 
        coords, randNum = calcCoords2(coords)
        
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

def quest22():
    global pause_event, stop_event

    wait_time = 5
    delay = random.uniform(0.8, 1.2)

    jwClick(1640, 960)
    time.sleep(delay)

    while True:

        oldCoords = [(1900, 950), (1872, 1012),  (1809,920), (1746,982),(1858,1015), (1783,915), (1881, 982)]
        newCoords = calcCoords2(oldCoords)
        for key, coords in enumerate(newCoords):
            if pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (219, 244, 178)):
                time.sleep(delay)
                jwClick(oldCoords)
                print(f"1 제출(녹색) {key}")

            elif pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (128,153,227)):
                time.sleep(1)
                jwClick(oldCoords)
                print(f"2 제출완료 {key}")
                time.sleep(wait_time)


            # 2 제출완료 이후에 실행되어야 하는 코드
                if pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (219,225,231)): #아이템을 눌러라
                    time.sleep(delay)
                    jwClick(1809,920)
                    print(f"2-1번 아이템")
                
                    time.sleep(1)
                    jwClick(1790,903)
                    print('Get 버튼')  

                    time.sleep(delay)
                    jwClick(1837,917)                
                    print('삼점으로 이동') 
              
                elif not pyautogui.pixelMatchesColor(1872, 1012, (128, 153, 227)): #퀘스트 제출이 완료되면 처음으로.
                    print(f"{wait_time}초간 반응이 없어 {1640, 960}를 클릭합니다.")
                    jwClick(1640, 960)

            elif pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (217,144,118)): 
                time.sleep(delay)
                jwClick(oldCoords)
                print(f"획득경로 1-1 {key}")

            elif pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (255,239,174)): 
                time.sleep(delay)
                jwClick(oldCoords)
                print(f"추천경로Clicked {key}") 

            elif pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (156,153,154)):
                time.sleep(delay)
                jwClick(oldCoords)
                print(f"플뤄스버튼 {key}") 

                time.sleep(delay)
                jwClick(1812,945)
                print('숫자2')

                time.sleep(delay)
                jwClick(1842,964)                
                print('숫자0')

                time.sleep(delay)
                jwClick(1845,981)
                print('녹색버튼')

                time.sleep(delay)
                jwClick(1750,1012)
                print('구매버튼')

                time.sleep(delay)
                jwClick(1899, 872)
                print('x 버튼')

                time.sleep(delay)
                jwClick(1640, 960)
                print('NPC 에게') 

            elif pyautogui.pixelMatchesColor(oldCoords[0], oldCoords[1], (217,144,118)): 
                time.sleep(delay)
                jwClick(oldCoords)
                print(f"획득경로 1-2 {key}") 

                time.sleep(delay)
                jwClick(1777,922)
                print('상점행')

                time.sleep(delay)
                jwClick(1744,929)
                print('숫자2')

                time.sleep(delay)
                jwClick(1786,949)                
                print('숫자0')

                time.sleep(delay)
                jwClick(1782,964)
                print('녹색버튼')

                time.sleep(delay)
                jwClick(1864,1012)
                print('구매버튼')

                time.sleep(delay)
                jwClick(1891, 868)
                print('x 버튼')

                time.sleep(delay)
                jwClick(1906, 874)
                print('x 버튼')

                time.sleep(delay)
                jwClick(1640, 960)
                print('NPC 에게')

        if stop_event.is_set():
            break  
           
   

# fishing_thread = threading.Thread(target=fishing)
# quest_thread = threading.Thread(target=quest)
# main_thread = fishing_thread

pauseFlag = True
main_thread = None  # main_thread 변수를 초기화합니다.

def fishing_start_button_clicked():
    global pauseFlag, start_button, main_thread
    if pauseFlag == True:
        if main_thread is None:
            selectMacro_clicked()
        stop_event.clear()
        if main_thread is not None:  # main_thread 변수가 None 값이 아닌 경우에만 start() 메소드를 호출합니다.
            main_thread.start()
        start_button['text'] = "■"

    else:
        stop_event.set()
        if main_thread is not None:
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
    elif cbSelectMacro.get() == '상퀘':
        main_thread = threading.Thread(target=quest22)

    ldplayerName = etWndName.get()

if __name__ == '__main__':
    root = tk.Tk()
    root.title(f"BanPoLoga {VERSION}")
    root.geometry("300x100+200+200")
    root.resizable(False, False)

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
        '일퀘',
        '상퀘',
     
    ]

    cbSelectMacro=tk.ttk.Combobox(root, height=15,width=10, values=macroList)
    cbSelectMacro.grid(row=1, column=1)
    cbSelectMacro.set("낚시")

    btnSelectMacro = tk.Button(root, text="설정", command=selectMacro_clicked)
    btnSelectMacro.grid(row=1, column=2)

    start_button = tk.Button(root, text="▶", command=fishing_start_button_clicked, width=15)
    start_button.grid(row=2, column=0)

    exit_button = tk.Button(root, text="종료", command=exit_button_clicked, width=15)
    exit_button.grid(row=3, column=0)

    puase_event.set()
 
    
    

    root.mainloop()