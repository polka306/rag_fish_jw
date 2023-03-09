import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui

img = cv2.imread('src_img1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
width, height = gray.shape[::-1]

screen = ImageGrab.grab()
np_screen = np.array(screen)
cv_screen = cv2.cvtColor(np_screen, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(cv_screen, gray, cv2.TM_SQDIFF)
val_min, val_max, min_loc, max_loc = cv2.minMaxLoc(result)
t_left = min_loc
b_right = (t_left[0] + width, t_left[1] + height)


cv2.rectangle(cv_screen,t_left, b_right, 255, 2)

cv2.imshow('src', gray)
cv2.imshow('screen', cv_screen)
cv2.waitKey()
cv2.destroyAllWindows()