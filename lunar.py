import os
import sys
import msvcrt
import threading

from lib.aimbot import Aimbot
from pynput import keyboard
from termcolor import colored

# CLI input:
#python lunar.py


def on_release(key):
    try:
        if key == keyboard.Key.f1:
            lunar.update_status_aimbot()
        if key == keyboard.Key.f2:
            lunar.clean_up()
    except NameError:
        pass

def main():
    global lunar
    lunar = Aimbot()
    lunar.start()

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

    print(colored('''
    | |
    | |    _   _ _ __   __ _ _ __
    | |   | | | | '_ \ / _` | '__|
    | |___| |_| | | | | (_| | |
    \_____/\__,_|_| |_|\__,_|_|

    (Neural-Network Aimbot)''', "yellow"))

    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
