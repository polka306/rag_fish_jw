import pyautogui
import time
import random
import os
import datetime

pyautogui.mouseInfo()

wait_time3 = 3

coords_2 = {'1' : (1650, 920), '2' : (1717, 935), '3' : (1780, 938), '4' : (1835, 928), '5' : (1877, 940), 
            '6' : (1652, 975), '7' : (1699, 990), '8' : (1754, 987), '9' : (1804, 985), '10' : (1857, 990)}

# 클릭 함수
def click(coord):
    pyautogui.click(coord[0], coord[1])

# RGB 값이 일치하는지 확인하는 함수
def check_color(coord1, expected_color):
    screenshot = pyautogui.screenshot()
    actual_color = screenshot.getpixel(coord1)
    return actual_color == expected_color


while True:
    now = datetime.datetime.now()
    if now.hour == 7 and now.minute == 0:
        pyautogui.doubleClick(1883, 944)
        break
        
    delay = random.uniform(0.8, 1.2)
    time.sleep(600)

if pyautogui.pixelMatchesColor(1822, 867, (136, 80, 128)):
        # 카니발 아이콘이 있을 때
     
        time.sleep(delay)
        pyautogui.click(1822, 867)
        print("카니발 클릭")

        time.sleep(delay)
        pyautogui.click(1761, 977)
        print('의뢰소 클릭')

        time.sleep(delay)
        pyautogui.click(1759, 1010)
        print('즉시이동')
        time.sleep(wait_time3)
        

elif not pyautogui.pixelMatchesColor(1822, 867, (136, 80, 128)):
        # 카니발 아이콘이 없을 때
        time.sleep(1)
        print(f"{wait_time3} 초간 반응이 없어 포링을 클릭합니다.")
        pyautogui.click(1859, 867)

        time.sleep(delay)
        pyautogui.click(1822, 867)
        print("카니발 클릭")

        time.sleep(delay)
        pyautogui.click(1761, 977)
        print('의뢰소 클릭')

        time.sleep(delay)
        pyautogui.click(1759, 1010)
        print('즉시이동')

        time.sleep(1)     

        flag=True   

# 좌표를 1초 간격으로 클릭
expected_color = (236, 112, 144)

time.sleep(15)

for i in range(1, 11):
    coord = coords_2[str(i)]
    
    if check_color((1872, 963), expected_color):
        click(coord)
        
    delay = random.uniform(1.3, 1.5)
    time.sleep(delay)
    print('퀘스트 수락')
    
    pyautogui.click(1757, 1001)
    time.sleep(delay)
    print('제출')
        

delay = random.uniform(1.2, 1.5)
time.sleep(delay)
pyautogui.click(1906, 870)
print("나가기 버튼")

time.sleep(delay)
pyautogui.click(1822, 867)
print("카니발 클릭")

time.sleep(delay)
pyautogui.click(1641, 932)
print("상점의뢰")

time.sleep(delay)
pyautogui.click(1761, 1010)
print("즉시이동")

time.sleep(3)

# 추가할 if 구문

if pyautogui.pixelMatchesColor(1900,986, (165,205,253)):
    time.sleep(delay)
    pyautogui.click(1905,985)
    print("상점 의뢰 수락") 

    time.sleep(delay)
    pyautogui.click(1840, 1010)
    print("수락")

    time.sleep(delay)
    pyautogui.click(1910, 873)
    print("나가기")

pyautogui.click(1620, 960)
delay = random.uniform(1.2, 1.5)
time.sleep(30)
    
coords_dict = {'1 제출(녹색)': (1900, 950),  
               '2제출완료': (1872, 1012), 
               '2-1 번 아이템': (1809,920),
               '플뤄스버튼': (1746,982),}

wait_time= 5
start_coord = (1640, 960)
    
while True:
    for key, coords in coords_dict.items(): #퀘스트를 수령한다.
        if pyautogui.pixelMatchesColor(coords[0], coords[1], (219, 244, 178)):
            time.sleep(1)
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
                pyautogui.click(1809,920)
                print(f"2-1번 아이템")
                
                time.sleep(1)
                pyautogui.click(1790,903)
                print('Get 버튼')  

                time.sleep(delay)
                pyautogui.click(1837,917)                
                print('삼점으로 이동') 
              
            elif not pyautogui.pixelMatchesColor(1872, 1012, (128, 153, 227)): #퀘스트 제출이 완료되면 처음으로.
                print(f"{wait_time}초간 반응이 없어 {start_coord}를 클릭합니다.")
                pyautogui.click(start_coord)

        elif pyautogui.pixelMatchesColor(coords[0], coords[1], (156,153,154)):
            time.sleep(1)
            pyautogui.click(coords)
            print(f"플뤄스버튼 {key}") 

            time.sleep(delay)
            pyautogui.click(1812,945)
            print('숫자2')

            time.sleep(delay)
            pyautogui.click(1842,964)                
            print('숫자0')

            time.sleep(delay)
            pyautogui.click(1845,981)
            print('녹색버튼')

            time.sleep(delay)
            pyautogui.click(1750,1012)
            print('구매버튼')

            time.sleep(delay)
            pyautogui.click(1899, 872)
            print('x 버튼')

            time.sleep(delay)
            pyautogui.click(1640, 960)
            print('NPC 에게')
    
        else:
        # 좌표 순회가 완료되었을 때 실행되는 부분
            pyautogui.click( 1640, 960 )
            delay = random.uniform(0.8, 1.1)
            time.sleep(60)
        continue
    
    break

# while 구문 이후에 와야 합니다.
while True:
    if condition:
        break

# 좌표 리스트
    coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
          (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
          (1878, 870), (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
          (1901, 952), (1819, 924), (1777, 997), (1899, 872),(1905, 985),
          (1905,933), ]    
          
       
# 좌표 순회
    for x, y in coords:
    # 좌표의 RGB값 가져오기
        r, g, b = pyautogui.pixel(x, y)

        x=random.randint(x, x+4)
        y=random.randint(y, y+4)

        e=random.randint(1620, 1660)
        w=random.randint(960, 963)

        p = random.uniform(2 , 4)


    # RGB값이 (255, 0, 0)인 경우 클릭        
        if (r, g, b) == (231,145,101):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay) 
            pyautogui.click(x, y)
            print("일퀘 클릭")          
            break
        
        elif (r, g, b) == (125,155,226):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("일퀘 완료 건네기 좌표")
            break

        elif (r, g, b) == (119, 88, 118):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("스킵 화살용 좌표")
            break

        elif (r, g, b) == (150, 226, 103):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("스킵 아래 녹색 좌표")
            break

        elif (r, g, b) == (255,248,230):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("황금 테두리 하얀손가락")
            break

        elif (r, g, b) == (206, 231,165):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("문답 지문 녹색2")            
            break

        elif (r, g, b) == (206,240,156):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("문답 지문 녹색1(위)+파란2 좌표")
            break

        elif (r, g, b) == (212,237,176):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("문답 지문 녹색1(위)+파란3 좌표")
            break

        elif (r, g, b) == (125,153,227):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("재료 건네기 좌표")
            break

        elif (r, g, b) == (205,232,164):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("문답 지문 녹색 좌표(1지문)")
            break

        elif (r, g, b) == (229,229,237):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("문답 지문 하얀색 좌표")
            break

        elif (r, g, b) == (231,229,232):
            delay = random.uniform(0.5, 1) 
            time.sleep(delay)
            pyautogui.click(x, y)
            print("일퀘 우측 나가기 버튼")
            break
    
    else:
        # 좌표 순회가 완료되었을 때 실행되는 부분

        pyautogui.click( e ,w , interval= p )
        


            
   




   

