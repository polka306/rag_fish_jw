import pyautogui
import time

pyautogui.mouseInfo()

coordinates_list = [
    [(1629, 949), (1617, 909), (1795, 976)],
    [(1675, 949), (1665, 909), (1722, 949)],
    [(1722, 949), (1709, 909), (1767, 949)],
    [(1767, 949), (1757, 909), (1814, 949)],
    [(1814, 949), (1802, 909), (1629, 1012)],
    [(1629, 1012), (1619, 974), (1675, 1012)],
    [(1675, 1012), (1665, 974), (1722, 1012)],
    [(1722, 1012), (1709, 974), (1784, 879)]]

while True:
    # 시작 좌표의 RGB 값 확인
    rgb = pyautogui.pixel(1909, 894)
    if rgb == (48,48,77):
        for coords in coordinates_list:
            pyautogui.click(coords[0][0],coords[0][1]) # 변수a 좌표 클릭
            pyautogui.sleep(1)
            print('길드 재료')

            rgb_guild = pyautogui.pixel(1909, 894) # 길드 버튼 RGB 값을 가져옴
            if rgb_guild != (48,48,77): # 길드 버튼 RGB가 맞지 않으면 다음 좌표로 이동
                print('길드 버튼 RGB가 맞지 않습니다.')
                continue
            else:
                pyautogui.click(1890, 1003) 
                pyautogui.sleep(1)
                print('제출')

                rgb1 = pyautogui.pixel(1890, 1003)
                if rgb1 == (120, 170, 87):
                    pyautogui.click(coords[1][0], coords[1][1]) # 변수b 좌표 클릭
                    pyautogui.sleep(1)
                    print('아이템 클릭')

                    pyautogui.click(1791, 902, interval=1) # Get 버튼
                    pyautogui.sleep(1)
                    print('Get 버튼 클릭')

                    pyautogui.click(x=1837, y=916, interval=1) # 추천 버튼(상점이동)
                    print('상점으로 이동')
                    pyautogui.sleep(20)
            
                    rgb2 = pyautogui.pixel(1889,882)             
                    if rgb2 == (125, 96 ,181):
                        pyautogui.click(x=1742, y=981, interval=1)
                        pyautogui.click(x=1807, y=959, interval=1)
                        pyautogui.click(x=1842, y=959, interval=1)
                        pyautogui.click(x=1842, y=976, interval=1)
                        pyautogui.click(x=1740, y=1009, interval=1)
                        pyautogui.click(x=1897, y=872, interval=1)
                        print('아이템 구매완료')
                        pyautogui.sleep(1)
                                    
                    else:                  
                        print("아이템 구매 완료 후 재확인")                   
                
                else:
                    # RGB 값이 일치하지 않으면 다음 좌표 클릭
                    pyautogui.click(coords[2][0], coords[2][1]) #1~8번까지 변수좌표 변수c
                    print('다음 좌표로 넘어가') 
                    pyautogui.sleep(1) 

                    pyautogui.click(1797,976) 
                    pyautogui.sleep(1)    
                    print('수정확인') 

 
    else:        
            rgb3 = pyautogui.pixel(1834, 957)
            if rgb3 == (107, 90, 129):
                pyautogui.click(1834, 957, interval=1)
                time.sleep(1)
                print('길드버튼')

                for pos in [ (1735, 886), (1687, 934)]:
                    pyautogui.click(pos, interval=1)
                    time.sleep(1)
                    print('길드 공헌')




                    