from ultralytics import YOLO
import pyautogui
import numpy as np
import cv2 as cv
import os
import time
import random
import string

# Constants
MODEL_PATH = 'best.pt'
SAVE_PATH = './databot/'
MAX_ATTEMPTS = 50

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def click(x, y):
    pyautogui.click(x, y, button='left')

def take_screenshot_and_save(x, y, w, h, c):
    p = random.randrange(15, 35)
    d = 2 * p
    rand1 = random.randrange(5, 25)
    rand2 = random.randrange(5, 25)
    x_poz = x - w / 2 - p
    y_poz = y - h / 2 - p
    im1 = pyautogui.screenshot(region=(x_poz, y_poz, w + d + rand1, h + d + rand2))
    fix = get_random_string(8)
    os.makedirs(f'{SAVE_PATH}/{c}/', exist_ok=True)
    im1.save(f"{SAVE_PATH}/{c}/{c} | {fix}.png")

def specialmenu(list):
    for item in list:
        if item not in chec

def main():
    model = YOLO(MODEL_PATH)
    list_cl = ['7-min5', 'train', 'baloon', 'chest', 'bonus-', 'accept-bonus-all']
    counter = 0
    while counter < MAX_ATTEMPTS:
        screen_img = pyautogui.screenshot()
        screen_img = np.array(screen_img)
        screen_img = cv.cvtColor(screen_img, cv.COLOR_RGB2BGR)
        results = model(screen_img)

        checklist = []
        list_menu = ['7-min', '7-min-null', '15-min', 'send-train-menu']
        for result in results:
            names = result.names
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                x, y, w, h = box.xywh[-1]
                c = names[box.cls.take(0)]
                checklist.append(c)

        for result in results:
            names = result.names
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                x, y, w, h = box.xywh[-1]
                c = names[box.cls.take(0)]
                # take_screenshot_and_save(x, y, w, h, c)
                # menucheck = ['5-min', '10-min']
                if '5-min' in checklist:
                    print(f"im in {c} click on a ")
                    try:
                        pyautogui.click('d7min.png')
                        break
                    except:
                        try:
                            pyautogui.click('d15min.png')
                            break
                        except:
                            pyautogui.click('d5min.png')
                            break
                    finally:
                        break

                # elif c in ['special-offer', 'info', 'window_7-min-unlock', 'window_bill-train', 'reconnect-need']:
                elif specialmenu(checklist):

                    for boxy in boxes:
                        x2, y2, _, _ = boxy.xywh[-1]
                        c2 = names[boxy.cls.take(0)]
                        if c2 == 'xx':
                            print(f"im in {c} click on a |{c2}|")
                            click(x2, y2)
                        elif c2 == 'bill-button-no-adds':
                            click(x2, y2)
                            print(f"im in {c} click on a |{c2}|")
                        elif c2 == 'reconnect':
                            click(x2, y2)
                            print(f"im in {c} click on a |{c2}|")

                # elif c == 'window_bill-train':
                #     for boxy in boxes:
                #         x2, y2, w2, h2 = boxy.xywh[-1]
                #         c2 = names[boxy.cls.take(0)]

                elif c in list_cl:
                    click(x, y)
                    print(f"click on a |{c}|")
                    break
                # elif c == 'xx' and list_menu not in checklist:
                #     click(x, y)
            break
        

        # counter += 1

    print("Done")

if __name__ == "__main__":
    main()
