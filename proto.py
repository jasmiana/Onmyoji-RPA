import pyautogui
import random
import time
import math

def _gaussian_click(center_x, center_y, radius=5):
    sigma = radius / 3
    r = min(abs(random.normalvariate(0, sigma)), radius)
    theta = random.uniform(0, 2 * math.pi)
    x = int(center_x + r * math.cos(theta))
    y = int(center_y + r * math.sin(theta))
    pyautogui.click(x, y)

def _click_series():
    decision = random.random()
    # sgm = 1
    # _bias_x, _bias_y = min((random.normalvariate(0, sgm)), -3), min((random.normalvariate(0, sgm)), -3)
    _now_x, _now_y = pyautogui.position()
    # _final_x = _now_x + _bias_x
    # _final_y = _now_y + _bias_y
    # pyautogui.moveTo(_final_x, _final_y)
    if decision > 0.665313:
        # pyautogui.click(_final_x, _final_y)
        _gaussian_click(_now_x, _now_y, 60)
    else:
        for _ in range(2):
            # pyautogui.click(_final_x, _final_y)
            _gaussian_click(_now_x, _now_y, 30)
            time.sleep(max(abs(random.normalvariate(0.09, 0.01)), 0.09))
    pyautogui.moveTo(_now_x, _now_y)

def _click_3():
    _now_x, _now_y = pyautogui.position()
    decision = random.random()
    if decision > 0.748964:
        for _ in range(3):
            _gaussian_click(_now_x, _now_y, 15)
            time.sleep(abs(random.normalvariate(0.1, 0.01)))
    else:
        for _ in range(4):
            _gaussian_click(_now_x, _now_y, 15)
            time.sleep(abs(random.normalvariate(0.1, 0.01)))
    pyautogui.moveTo(_now_x, _now_y)

if __name__ == "__main__":
    for i in range(3, 0, -1):
        print(f"Start in {i} s...", end="\r")
        time.sleep(1)
    print("\nStart...")
    
    FLAG = 1
    
    while True:
        try:
            des1 = random.random()
            des2 = random.normalvariate(-0.1, 0.5)
            
            if FLAG == 1:
                _click_series()
                time.sleep(max(abs(random.normalvariate(10.5, 2)), 10))
                
            if des1 > des2:
                _click_series()
                time.sleep(max(abs(random.normalvariate(1.2, 0.2)), 1))
                FLAG = 1
            else:
                _click_3()
                time.sleep(max(abs(random.normalvariate(12.5, 2)), 12))
                FLAG = 0
        except pyautogui.PyAutoGUIException as e:
            print("⚠️ Fail Safe Exception")
            break
        
        # _click_3()
        # time.sleep(max(abs(random.normalvariate(10.5, 2)), 10))