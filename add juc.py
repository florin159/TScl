import pyautogui

# button7location = pyautogui.locateOnScreen('calc7key.png')
# button7location
# Box(left=1416, top=562, width=50, height=41)
# button7location[0]
# 1416
# button7location.left
# 1416
# button7point = pyautogui.center(button7location)
# button7point
# Point(x=1441, y=582)
# button7point[0]
# 1441
# button7point.x
# 1441
# button7x, button7y = button7point
# pyautogui.click(button7x, button7y)  # clicks the center of where the 7 button was found


for pos in pyautogui.locateAllOnScreen('add.png'):
   print(pos)

xx = list[pyautogui.locateAllOnScreen('add.png')] # a shortcut version to click on the center of where the 7 button was found

# xx = xx[1]
print(xx)
