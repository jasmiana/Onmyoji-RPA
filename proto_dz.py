import pyautogui
import random
import time
import math
import sys
import cv2
import numpy as np

def find_and_click_image(image_path="pic4.png", threshold=0.6, max_attempts=6):
    """
    检测屏幕中是否出现指定图片（支持等比例缩放），若找到则在图片范围内随机位置点击 1~2 次。
    最多尝试 max_attempts 次，未检测到则等待（0.1s, 0.2s, 0.4s...）后重试。
    """
    template = cv2.imread(image_path, 0)
    if template is None:
        print(f"[{time.strftime('%m/%d %H:%M:%S')}] - ⚠️  无法读取图片文件: {image_path}")
        return False
        
    wait_time = 0.2
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            print(f"[{time.strftime('%m/%d %H:%M:%S')}] - 未检测到图片，等待 {wait_time}s 后进行第 {attempt} 次尝试...", end="\r")
            time.sleep(wait_time)
            wait_time *= 2

        # 获取屏幕尺寸，计算第四象限（右下角）的坐标和宽高
        screen_width, screen_height = pyautogui.size()
        q4_x, q4_y = screen_width // 2, screen_height // 2
        q4_w, q4_h = screen_width - q4_x, screen_height - q4_y

        # 只对第四象限进行截图
        screenshot = pyautogui.screenshot(region=(q4_x, q4_y, q4_w, q4_h))
        screen_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        
        best_max_val = -1
        best_loc = None
        best_scale = 1.0
        best_shape = None
        
        # 在 0.2 到 1.0 倍数之间尝试多种缩放比例
        for scale in np.linspace(0.35, 1, 13)[::-1]:
            resized_template = cv2.resize(template, (int(template.shape[1]*scale), int(template.shape[0]*scale)))
            # 确保缩放后的模板小于或等于屏幕尺寸
            if resized_template.shape[0] > screen_gray.shape[0] or resized_template.shape[1] > screen_gray.shape[1]:
                continue
                
            result = cv2.matchTemplate(screen_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > threshold and max_val > best_max_val:
                best_max_val = max_val
                best_loc = max_loc
                best_scale = scale
                best_shape = resized_template.shape
                
        if best_max_val > threshold:
            x, y = best_loc
            h, w = best_shape
            
            # 记录当前鼠标位置
            original_x, original_y = pyautogui.position()
            
            # 在范围内任意一个位置（注意加上第四象限的起始偏移 q4_x, q4_y）
            target_x = q4_x + x + random.randint(0, w)
            target_y = q4_y + y + random.randint(0, h)
            
            if attempt > 1:
                # 清除同一行上重试留下的输出
                print(" " * 80, end="\r")
            
            print(f"[{time.strftime('%m/%d %H:%M:%S')}] - 检测到 - Scale {best_scale:.2f} Confidence {best_max_val:.2f} -> Clicking ({target_x}, {target_y})", end="\r")
            
            # 自动点击一次或两次
            clicks = random.choice([1, 2])
            for _ in range(clicks):
                # _gaussian_click(target_x, target_y, radius=max(min(w, h)//10, 5))
                pyautogui.click(target_x, target_y)
                if clicks > 1:
                    time.sleep(abs(min(max(random.normalvariate(0.07, 0.01), 0.06), 0.1)))
                    
            # 移回点击前的鼠标位置
            pyautogui.moveTo(original_x, original_y)
            
            return True
            
    if max_attempts > 1:
        print(" " * 80, end="\r")
        print(f"[{time.strftime('%m/%d %H:%M:%S')}] - 连续 {max_attempts} 次未检测到图片，放弃尝试。")
        
    return False

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
    try:
        for i in range(3, 0, -1):
            print(f"[{time.strftime('%m/%d %H:%M:%S')}] - Start in {i} s...", end="\r")
            time.sleep(1)
        print(f"\n[{time.strftime('%m/%d %H:%M:%S')}] - Start...")
    except KeyboardInterrupt:
        print("")
        print(f"[{time.strftime('%m/%d %H:%M:%S')}] - ⚠️  Ctrl+C")
        sys.exit(0)
    
    count = 0
    while True:
        try:                
            des1 = [random.random() for _ in range(20)]
            des2 = random.sample(range(20), 6) # random.sample(population, k) 会从 population 中无放回地随机抽取 k 个不同元素
            
            _click_series()
            # time.sleep(max(abs(random.normalvariate(16.5, 0.25)), 16))  # dz
            time.sleep(min(max(abs(random.normalvariate(12, 0.4)), 11.2), 12.4))  # ylg
            # time.sleep(max(abs(random.normalvariate(13.5, 0.25)), 13))  # HD

            if des1[des2[2]] > des1[des2[3]]:
                _click_series()
            else:
                _click_3()
            time.sleep(min(max(abs(random.normalvariate(1.2, 0.1)), 1), 1.5))
            
            # 尝试检测并点击目标图片
            if find_and_click_image("pic4.png"):
                time.sleep(max(abs(random.normalvariate(0.3, 0.05)), 0.2))

            if des1[des2[4]] > des1[des2[5]]:
                _click_series()
            else:
                _click_3()
            time.sleep(min(max(abs(random.normalvariate(1.3, 0.15)), 1), 1.5))  # dz

            count += 1
            if count % 10 == 0:
                print(f"\n[{time.strftime('%m/%d %H:%M:%S')}] - Count: {count}")
            
        except pyautogui.PyAutoGUIException:
            print(f"\n[{time.strftime('%m/%d %H:%M:%S')}] - ⚠️  Fail Safe Exception")
            print(f"\n[{time.strftime('%m/%d %H:%M:%S')}] - Count: {count}")
            sys.exit(0)   
        except KeyboardInterrupt:
            print(f"\n[{time.strftime('%m/%d %H:%M:%S')}] - ⚠️  Ctrl+C")
            print(f"\n[{time.strftime('%m/%d %H:%M:%S')}] - Count: {count}")
            sys.exit(0)   
        
        # _click_3()
        # time.sleep(max(abs(random.normalvariate(10.5, 2)), 10))

