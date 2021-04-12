import os
import sys
import msvcrt
import threading

from lib.aimbot import Aimbot
from pynput import keyboard

# CLI input:
#python lunar.py


def on_release(key):
    try:
        if key == keyboard.Key.f1:
            lunar.update_status_aimbot()
        if key == keyboard.Key.esc:
            lunar.clean_up()
    except NameError:
        pass

def main():
    global lunar
    lunar = Aimbot()
    lunar.start()

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

    print('''
    ====================================
        Lunar (Neural-Network Aimbot)
    ====================================
    ''')

    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
