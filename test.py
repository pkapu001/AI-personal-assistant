import keyboard
from threading import Thread


keyboard.add_hotkey('ctrl+r', print, args=('key press'), suppress=True)
while True:
    a = 1
