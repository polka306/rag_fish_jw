import pyautogui
import time
import os
import random

#pyautogui.mouseInfo()

# file_list = os.listdir(os.path.realpath("img\\"))


while True:

# 좌표 리스트
    coords = [(1646, 935),(1725, 940),(1786, 949),(1824, 945),(1886, 955),
          (1634, 989),(1694, 1002),(1744, 995),(1804, 1000),(1852, 1005),
          (1878, 870), (1882, 1028), (1899, 985), (1899, 985), (1869, 1012),
          (1901, 952), (1819, 924), (1777, 997), (1899, 872),(1905, 985),]    
          
       
# 좌표 순회
    for x, y in coords:
    # 좌표의 RGB값 가져오기
        r, g, b = pyautogui.pixel(x, y)

        x=random.randint(x, x+4)
        y=random.randint(y, y+4)

        e=random.randint(1620, 1660)
        w=random.randint(960, 963)

        p = random.uniform(4 , 6)


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
        



           


         

        
