from ultralytics import YOLO
import pyautogui
import numpy as np
import cv2 as cv
import os
import time
import random
import string
import win32gui, win32ui, win32con, win32api

# Constants
MODEL_PATH = 'best.pt'
SAVE_PATH = './databot/'
MAX_ATTEMPTS = 50

#backup
def get_screen_shot():
    h = 635
    w = 1925
    # hwnd = None
    hwnd = win32gui.FindWindow(None, 'TrainStation - Pixel Federation Games - Opera')
    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (335, 165), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    img = img[...,:3]

    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    img = np.ascontiguousarray(img)

    return img

def get_screenshot():
    h = 800
    w = 2260
    # hwnd = None
    hwnd = win32gui.FindWindow(None, 'TrainStation - Pixel Federation Games - Opera')
    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    img = img[...,:3]

    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    img = np.ascontiguousarray(img)

    return img

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def click(x, y):
    # pyautogui.click(x, y, button='left')
    x = int(x)
    y = int(y)

    # Get the handle of the window
    hwnd = win32gui.FindWindow(None, 'TrainStation - Pixel Federation Games - Opera')

    # Bring the window to the foreground
    win32gui.SetForegroundWindow(hwnd)

    # Set the cursor position
    win32api.SetCursorPos((x,y))

    # Simulate a left mouse button click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

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

def main():
    model = YOLO(MODEL_PATH)
    list_cl = ['7-min5', 'train', 'baloon', 'chest', 'bonus-', 'accept-bonus-all']
    counter = 0
    while counter < MAX_ATTEMPTS:
        # screen_img = pyautogui.screenshot()
        # screen_img = np.array(screen_img)
        # screen_img = cv.cvtColor(screen_img, cv.COLOR_RGB2BGR)

        screen_img = get_screenshot()
        results = model(screen_img)
        # if pyautogui.locateOnScreen('baloon.png'):
        #     pyautogui.click('baloon.png')
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
                if '5-min' in checklist or '10-min' in checklist:
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


                elif 'ballon' in checklist:
                    pyautogui.click('baloon.png')
                elif c in ['special-offer', 'info', 'window_7-min-unlock', 'window_bill-train', 'reconnect-need']:
                # elif specialmenu(checklist):
                    # print('aprove_____________________')
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
                        else:
                            click(1605, 310)
                            # xx_SO_2.png


                # elif c == 'window_bill-train':
                #     for boxy in boxes:
                #         x2, y2, w2, h2 = boxy.xywh[-1]
                #         c2 = names[boxy.cls.take(0)]

                elif c in list_cl:
                    try:
                        pyautogui.click('baloon.png')
                        break
                    except:
                        click(x, y)
                        time.sleep(0.3)
                        print(f"click on a |{c}|")
                        break
                # elif c == 'xx' and list_menu not in checklist:
                #     click(x, y)
            break
        

        # counter += 1

    print("Done")

if __name__ == "__main__":
    main()
