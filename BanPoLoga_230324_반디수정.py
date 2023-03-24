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

import lib.jw_log as jwlog

DEBUG = False

VERSION = "230324"

ldplayerName ="LDPlayer"
#ldplayerName ="포샵"
log = jwlog.jw_make_logger(f"BanPoLoga_{VERSION}")
log.setLevel(jwlog.logging.DEBUG)

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

def calcCoordsFromConfig(config, key, subkey=None, relative=False):
    global ldplayerName

    hwnd = win32gui.FindWindow(None, ldplayerName)

    newCoords = []

    if hwnd >=1:    
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right -left
        h = bot - top

        log.debug(f"hwnd = {left}, {top}, {w}, {h}")
        if subkey is None:
            for name, ratio in config.values[key].coords.items():
                if(relative):
                    newCoords.append((round(w*ratio[0]), round(h*ratio[1])))
                else:
                    newCoords.append((round(left + w*ratio[0]), round(top + h*ratio[1])))
                log.debug(f"{name} : {newCoords[-1]}")
        else :
            for idx, ratio in enumerate(config.values[key].coords[subkey]):
                if(relative):
                    newCoords.append((round(w*ratio[0]), round(h*ratio[1])))
                else:
                    newCoords.append((round(left + w*ratio[0]), round(top + h*ratio[1])))
                log.debug(f"{idx} : {newCoords[-1]}")

    return newCoords

def getPixelWnd(x, y, size=1):
    pixels = []
    for i in range(x-size, x+size+1):
        for j in range(y-size, y+size+1):
            try:
                pixels.append(pyautogui.pixel(i, j))
            except:
                log.error("픽셀값을 얻을 수 없습니다.")
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
        log.debug(f"click {x}, {y}")
        pos = (x,y)
        cli_pos = win32gui.ScreenToClient(hwnd, pos)
        lParam = win32api.MAKELONG(cli_pos[0]-1, cli_pos[1]-34)
        hWnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

conf = JsonConfigFileManager('./config.json')
ldplayerName = conf.values.windowName

def fishing():
    global puase_event, stop_event, conf
    step = 1
    fail_count = 0 
    error_count = 0
    success_count = 0
    log.info(f"낚시 시작")
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
                log.info("낚시 시작")
            else:
                fail_count += 1
        elif step==2:
            if(findColorinPixels(pixels, (229,222,243))):
                step = 3
                fail_count = 0
                log.info("낚시 중")
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
                success_count += 1
                log.info(f"낚시 성공, 총 {success_count}회 낚시 성공 했습니다.")
            else:
                fail_count += 1

        if fail_count > 50 :
            step = 1
            fail_count = 0
            error_count += 1
            log.error("에러발생함")
        
        if error_count > 10 and error_exit_box.get() :
            log.error(f"에러발생횟수 = {error_count}, 낚시멈춤 체크박스 = {error_exit_box.get()}")
            log.error("에러가 10번 발생하여 낚시를 중지합니다.")
            break

        if stop_event.is_set():
            break

def quest():
    global stop_event, conf
    notice_board = 0
    check_findcolor = 0
    check_count_success = 0
    log.info(f"일퀘 시작")
    while True:
        coords = calcCoordsFromConfig(conf,'quest')
        randNum = [
            (coords[-2][0], coords[-2][1]),
            (coords[-1][0], coords[-1][1])
        ]
        coords.remove(randNum[0])
        coords.remove(randNum[1])
        delay = random.uniform(0.1, 0.5)
        
    # 좌표 순회
        for idx, pos in enumerate(coords):
            x = pos[0]
            y = pos[1]
            # 좌표의 RGB값 가져오기
            # r, g, b = pyautogui.pixel(x, y)
            pixels = getPixelWnd(x, y, 1)

            # if(DEBUG): print(f"{coords.index((x,y))} ({x}, {y}) : {pixels}")

            x=random.randint(x, x+4)
            y=random.randint(y, y+4)

            e=random.randint(randNum[0][0], randNum[1][0])
            w=random.randint(randNum[0][1], randNum[1][1])

            p = random.uniform(4 , 6)
            
            if(notice_board == 0) :
                if findColorinPixels(pixels, (231,145,101)):  
                    jwClick(x, y)
                    notice_board = 1
                    log.info(f"(Pos idx:{idx}) 일퀘 클릭")   

                elif findColorinPixels(pixels, (119, 88, 118)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 스킵 화살용 좌표")
                    check_findcolor = 1

                elif findColorinPixels(pixels, (150, 226, 103)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 스킵 아래 녹색 좌표")

                elif findColorinPixels(pixels, (255,248,230)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 황금 테두리 하얀손가락")


                elif findColorinPixels(pixels, (206, 231,165)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 문답 지문 녹색2")            


                elif findColorinPixels(pixels, (206,240,156)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 문답 지문 녹색1(위)+파란2 좌표")


                elif findColorinPixels(pixels, (212,237,176)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 문답 지문 녹색1(위)+파란3 좌표")


                elif findColorinPixels(pixels, (125,153,227)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 재료 건네기 좌표")


                elif findColorinPixels(pixels, (205,232,164)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 문답 지문 녹색 좌표(1지문)")


                elif findColorinPixels(pixels, (229,229,237), (1,1,1)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 문답 지문 하얀색 좌표 = {x}, {y}")

                elif findColorinPixels(pixels, (231,229,232), (1,1,1)):
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 일퀘 우측 나가기 버튼")
                    check_findcolor = 1
                else :
                    check_findcolor = 1
            elif notice_board == 1 :
                if findColorinPixels(pixels, (125,155,226)):
                    notice_board = 2
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 일퀘 완료 건네기 좌표")
                    check_findcolor = 0           
            elif notice_board == 2 :
                if findColorinPixels(pixels, (231,229,232), (1,1,1)):
                    notice_board = 0
                    jwClick(x, y)
                    log.info(f"(Pos idx:{idx}) 일퀘 우측 나가기 버튼")
                    check_findcolor = 1
                    check_count_success += 1
                    log.info(f"(Pos idx:{idx}) 이때까지 완료한 퀘스트 갯수 : {check_count_success}")
            
        if check_findcolor == 1 :
            time.sleep(delay)
            jwClick(e, w) # 좌측 일퀘 진행 부분 클릭
            log.info(f"pos : {e}, {w} 퀘스트 진행 클릭")
            time.sleep(p)
            check_findcolor = 0
        else :
            time.sleep(delay)
            check_findcolor = 1
        
        if check_count_success == 10 and success_exit_box.get() :
            log.info(f"퀘스트 성공 횟수 : {check_count_success} , 체크박스 : {success_exit_box.get()}")
            log.info(f"(Pos idx:{idx}) 퀘스트를 10번 완료 하여 종료 합니다.")
            break

        if stop_event.is_set():
            break

def merchant_quest():
    global stop_event, conf
    log.info(f"상점퀘 시작")
    wait_time= 5
    start_coord = calcCoordsFromConfig(conf, "merchant_quest", subkey="start")
    x_s, y_s = start_coord[0]
    delay = random.uniform(0.8, 1.2)
    select_merchant = 0
    sucsses_count = 0

    jwClick(x_s,y_s)
    time.sleep(delay)

    while True:
        delay = random.uniform(0.8, 1.2)
        coords_dict = {'1 제출(녹색)': (1900, 950),  
               '2제출완료': (1872, 1012), 
               '2-1 번 아이템': (1809,920),
               '플뤄스버튼': (1746,982),
               '획득경로':(1858,1015),
               '추천경로':(1783,915),
               '직구':(1881, 982),}
        
        coords = calcCoordsFromConfig(conf, "merchant_quest", subkey="coords")

        x_start_coords, y_start_coords = coords[1]

        coords_select_merchant = calcCoordsFromConfig(conf, "merchant_quest", subkey="coords_select_merchant")
        coords_select_merchant_list = ['일반상점', '아가미상점']        

        coords_after_send = calcCoordsFromConfig(conf, "merchant_quest", subkey="coords_after_send")
        x_after_send, y_after_send = coords_after_send[0]        
        coords_after_send_list = ['2-1번 아이템', 'Get 버튼', '삼점으로 이동',]

        coords_buy_1 = calcCoordsFromConfig(conf, "merchant_quest", subkey="coords_buy_1")
        coords_buy_1_list = ['숫자2', '숫자0', '녹색버튼', '구매버튼', 'x버튼', 'npc에게',]

        coords_buy_2 = calcCoordsFromConfig(conf, "merchant_quest", subkey="coords_buy_2")
        coords_buy_2_list = [('숫자1'), ('숫자5'),('녹색버튼'), ('구매버튼'), 
                             ('x버튼'), ('x버튼'), ('npc에게'),]
        
        #for x, y in coords : #퀘스트를 수령한다.
        for idx, pos in enumerate(coords):
            x = pos[0]
            y = pos[1]

            if findColorinPixels(getPixelWnd(x,y,0), (219, 244, 178)):
                time.sleep(delay)
                jwClick(x,y)
                log.info(f"(Pos idx:{idx})  상점스태프 아이템 클릭")

            elif findColorinPixels(getPixelWnd(x,y,0), (128,153,227)): #퀘스트를 제출한다.
                time.sleep(1)
                jwClick(x,y)
                log.info(f"(Pos idx:{idx}) 아이템 제출완료")                
                sucsses_count += 1
                log.info(f"(Pos idx:{idx}) 현재까지 완료된 상점 퀘스트는 : {sucsses_count} 번 입니다.")
                time.sleep(wait_time)

                # 2 제출완료 이후에 실행되어야 하는 코드

                #아이템이 이미 가방에 존재 할때 실행 
                if findColorinPixels(getPixelWnd(x_after_send,y_after_send,0), (219,225,231)): #아이템을 눌러라
                    after_send_count = 0
                    sucsses_count -= 1
                    log.info(f"(Pos idx:{idx}) 아이템이 모자라서 완료 횟수를 차감합니다.")
                    log.info(f"(Pos idx:{idx}) 현재까지 완료된 상점 퀘스트는 : {sucsses_count} 번 입니다.")
                    for x_1,y_1 in coords_after_send :
                        time.sleep(delay)
                        jwClick(x_1,y_1)
                        log.info(f"(Pos idx:{idx}) 아이템을 구입하러 상점으로 갑니다")
                        log.info(f"(Pos idx:{idx}) 현재 실행 : {coords_after_send_list[after_send_count]}")                        
                        after_send_count += 1
                        select_merchant = 1
                elif not findColorinPixels(getPixelWnd(x_start_coords, y_start_coords,0), (128, 153, 227)): #퀘스트 제출이 완료되면 처음으로.
                    log.info(f"(Pos idx:{idx}) {wait_time}초간 반응이 없어 퀘스트 창을 클릭합니다.")
                    jwClick(x_s,y_s)

            elif findColorinPixels(getPixelWnd(x,y,0), (217,144,118)): 
                jwClick(x,y)
                log.info(f"획득경로 확인 중입니다")
                time.sleep(delay)
                
                select_x,select_y = coords_select_merchant[0]                
                if findColorinPixels(getPixelWnd(select_x,select_y,0), (255,239,174)):
                    time.sleep(delay)
                    jwClick(select_x,select_y)
                    log.info(f"(Pos idx:{idx}) 경로는  {coords_select_merchant_list[0]}")
                    select_merchant = 1
                select_x,select_y = coords_select_merchant[1]
                if not findColorinPixels(getPixelWnd(select_x,select_y,0), (255,239,174)): 
                    log.info(f"(Pos idx:{idx}) 경로는  {coords_select_merchant_list[1]}")
                    jwClick(select_x,select_y)
                    select_merchant = 2
            #elif findColorinPixels(getPixelWnd(getPixelWnd(x,y, (255,239,174)): 
            #    time.sleep(delay)
            #    jwClick(x,y)
            #    log.info(f"(Pos idx:{idx}) 추천경로Clicked") 
            
            # 로가 기준 
            #elif findColorinPixels(getPixelWnd(getPixelWnd(x,y, (156,153,154)):
            # 반디 기준 
            elif (findColorinPixels(getPixelWnd(x,y,0), (121,110,113)) & (select_merchant==1)):
                time.sleep(delay)
                jwClick(x,y)                
                log.info(f"(Pos idx:{idx}) 아이템을 구입하러 상점으로 갑니다. ")
                buy_1_count=0
                for x_2,y_2 in coords_buy_1 :
                    time.sleep(delay)
                    jwClick(x_2, y_2)
                    log.info(f"(Pos idx:{idx}) 현재 실행 : {coords_buy_1_list[buy_1_count]}")
                    buy_1_count += 1

            elif (findColorinPixels(getPixelWnd(x,y,0), (121,110,113)) & (select_merchant==2)):
                time.sleep(delay)
                jwClick(x,y)
                log.info(f"(Pos idx:{idx}) 아이템을 구입하러 상점스태프에게 갑니다.") 
                buy_2_count=0
                for x_3,y_3 in coords_buy_2 :
                    time.sleep(delay)
                    jwClick(x_3, y_3)
                    log.info(f"(Pos idx:{idx}) 현재 실행 : {coords_buy_2_list[buy_2_count]}")
                    buy_2_count += 1
        
        if sucsses_count == 10 and success_exit_box.get() :
            log.info(f"퀘스트 성공 횟수 : {sucsses_count} , 체크박스 : {success_exit_box.get()}")
            log.info(f"(Pos idx:{idx}) 퀘스트를 10번 완료 하여 종료 합니다.")
            break

        if stop_event.is_set():
            break

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
    if main_thread is not None and main_thread.is_alive():
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
    elif cbSelectMacro.get() == '상점퀘':
        main_thread = threading.Thread(target=merchant_quest)

    ldplayerName = etWndName.get()
    conf.update({'windowName':ldplayerName})
    conf.export('./config.json')

def checkPoint_clicked():
    th = threading.Thread(target=checkPoint)
    th.start()

def checkPoint():
    global conf
    conf.reload()
    if cbSelectMacro.get() == '낚시':
        coords = calcCoordsFromConfig(conf, "fishing", relative=True)
    elif cbSelectMacro.get() == '일퀘':
        coords = calcCoordsFromConfig(conf, "quest", relative=True)
    elif cbSelectMacro.get() == '상점퀘':
        coords = []
        for subkey in conf.values.merchant_quest.coords.keys():
            coords.extend(calcCoordsFromConfig(conf, "merchant_quest", subkey=subkey, relative=True))

    hwndname = ldplayerName
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
    else:
        log.error(f"{hwndname} 창을 찾을 수 없습니다.")
        return

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
            log.debug(f"{idx}:{pyautogui.pixel(left+pos[0],top+pos[1])}")
        im.show()

if __name__ == '__main__':

    root = tk.Tk()
    root.title(f"BanPoLoga {VERSION}")
    root.geometry("400x100+200+200")
    # root.resizable(False, False)

    lbWndName=tk.Label(root, text="창 이름:", width=10)
    lbWndName.grid(row=0, column=0)

    etWndName = tk.Entry(root, width=15)
    etWndName.bind("<Return>", setWindowName)
    etWndName.grid(row=0, column=1,sticky="we")
    etWndName.insert(0, ldplayerName)

    lbSelMacro=tk.Label(root, text="매크로 선택:", width=10)
    lbSelMacro.grid(row=1, column=0)

    macroList = [
        '낚시',
        '일퀘',
        '상점퀘'
    ]

    cbSelectMacro=tk.ttk.Combobox(root, height=15,width=15, values=macroList)
    cbSelectMacro.grid(row=1, column=1,sticky="we")
    cbSelectMacro.set("낚시")

    btnSelectMacro = tk.Button(root, text="설정", command=selectMacro_clicked)
    btnSelectMacro.grid(row=1, column=2,sticky="we")

    btnCheckPoint = tk.Button(root, text="좌표확인", command=checkPoint_clicked)
    btnCheckPoint.grid(row=1, column=3,sticky="we")

    start_button = tk.Button(root, text="▶", command=start_button_clicked, width=15)
    start_button.grid(row=2, column=0,sticky="we")

    exit_button = tk.Button(root, text="종료", command=exit_button_clicked, width=15)
    exit_button.grid(row=3, column=0,sticky="we")

    error_exit_box = tk.IntVar()
    error_chk = tk.Checkbutton(root, text="낚시 : 에러 10번나면 멈춤", variable=error_exit_box, onvalue=1, offvalue=0)
    error_chk.grid(row=2, column=1,sticky="w")

    success_exit_box = tk.IntVar()
    success_chk = tk.Checkbutton(root, text="퀘스트 : 10번 완료되면 멈춤", variable=success_exit_box, onvalue=1, offvalue=0)
    success_chk.grid(row=3, column=1,sticky="w")

    puase_event.set()

    root.mainloop()