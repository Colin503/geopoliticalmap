import pyautogui
import time

print("Pose ta souris sur le coin HAUT-GAUCHE de la zone, attends 2 sec.")
time.sleep(2)
x1, y1 = pyautogui.position()
print(f"Coin 1 : {x1}, {y1}")

print("Pose ta souris sur le coin BAS-DROIT de la zone, attends 2 sec.")
time.sleep(2)
x2, y2 = pyautogui.position()
print(f"Coin 2 : {x2}, {y2}")

width = x2 - x1
height = y2 - y1
print(f"Copie ça dans ton code : ({x1}, {y1}, {width}, {height})")