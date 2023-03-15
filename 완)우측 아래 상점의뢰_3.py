import pyautogui
import time
import random

#pyautogui.mouseInfo()

coords_dict = {'1 제출(녹색)': (1900, 950),  
               '2제출완료': (1872, 1012), 
               '2-1 번 아이템': (1809,920),
               '플뤄스버튼': (1746,982),
               '획득경로':(1858,1015),
               '추천경로':(1783,915),
               '직구':(1881, 982),}
wait_time= 5
start_coord = (1640, 960)

xx=random.randint(1, 3)
yy=random.randint(1, 3)

delay = random.uniform(0.8, 1.2)

pyautogui.click(start_coord)
time.sleep(delay)

while True:
    for key, coords in coords_dict.items(): #퀘스트를 수령한다.
        if pyautogui.pixelMatchesColor(coords[0], coords[1], (219, 244, 178)):
            time.sleep(delay)
            pyautogui.click(coords)
            print(f"1 제출(녹색) {key}")

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (128,153,227)): #퀘스트를 제출한다.
            time.sleep(1)
            pyautogui.click(coords)
            print(f"2 제출완료 {key}")
            time.sleep(wait_time)

            # 2 제출완료 이후에 실행되어야 하는 코드
            if pyautogui.pixelMatchesColor(1809,920, (219,225,231)): #아이템을 눌러라
                time.sleep(delay)
                pyautogui.click(1809+xx,920+yy)
                print(f"2-1번 아이템")
                
                time.sleep(1)
                pyautogui.click(1790+xx,903)
                print('Get 버튼')  

                time.sleep(delay)
                pyautogui.click(1837+xx,917+yy)                
                print('삼점으로 이동') 
              
            elif not pyautogui.pixelMatchesColor(1872, 1012, (128, 153, 227)): #퀘스트 제출이 완료되면 처음으로.
                print(f"{wait_time}초간 반응이 없어 {start_coord}를 클릭합니다.")
                pyautogui.click(start_coord)

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (217,144,118)): 
            time.sleep(delay)
            pyautogui.click(coords)
            print(f"획득경로Clicked {key}")

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (255,239,174)): 
            time.sleep(delay)
            pyautogui.click(coords)
            print(f"추천경로Clicked {key}") 

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (156,153,154)):
            time.sleep(delay)
            pyautogui.click(coords)
            print(f"플뤄스버튼 {key}") 

            time.sleep(delay)
            pyautogui.click(1812+xx,945+yy)
            print('숫자2')

            time.sleep(delay)
            pyautogui.click(1842+xx,964+yy)                
            print('숫자0')

            time.sleep(delay)
            pyautogui.click(1845+xx,981+yy)
            print('녹색버튼')

            time.sleep(delay)
            pyautogui.click(1750+xx,1012+yy)
            print('구매버튼')

            time.sleep(delay)
            pyautogui.click(1899+xx, 872+yy)
            print('x 버튼')

            time.sleep(delay)
            pyautogui.click(1640+xx, 960)
            print('NPC 에게') 

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (121,110,113)):
            time.sleep(delay)
            pyautogui.click(coords)
            print(f"직구 {key}") 

            time.sleep(delay)
            pyautogui.click(1744+xx,929+yy)
            print('숫자2')

            time.sleep(delay)
            pyautogui.click(1786+xx,949+yy)                
            print('숫자0')

            time.sleep(delay)
            pyautogui.click(1782+xx,964+yy)
            print('녹색버튼')

            time.sleep(delay)
            pyautogui.click(1864+xx,1012+yy)
            print('구매버튼')

            time.sleep(delay)
            pyautogui.click(1891+xx, 868+yy)
            print('x 버튼')

            time.sleep(delay)
            pyautogui.click(1906+xx, 874+yy)
            print('x 버튼')

            time.sleep(delay)
            pyautogui.click(1640+xx, 960)
            print('NPC 에게')


            
   