import os
import sys
import msvcrt
import threading
from pynput.keyboard import Key, Listener

from termcolor import colored
from lib.detect import Detect

# CLI input:
#python lunar.py



def on_release(key):
    global AIMBOT_STR
    if key == Key.f1:
        if AIMBOT_STR == colored("ENABLED", 'green'):
             AIMBOT_STR = colored("DISABLED", 'red')
             sys.stdout.write("\033[K")
             print(update_output(AIMBOT_STR), end='\r')
        else:
            AIMBOT_STR = colored("ENABLED", 'green')
            sys.stdout.write("\033[K")
            print(update_output(AIMBOT_STR), end='\r', flush=True)
    if key == Key.esc:
        print("ESCAPE WAS PRESSED. QUITTING...")
        sys.exit()


def keyboard_listener():
    with Listener(on_release=on_release) as listener:
        listener.join()


def main():
    print("[INFO] Loading the neural network model")
    aimbot_obj = Detect()

    print("[INFO] Beginning screen capture")
    aimbot_obj.detect_screen()

    print("\n[INFO] PRESS 'F1' TO TOGGLE AIMBOT\n[INFO] PRESS 'ESCAPE' TO QUIT")


if __name__ == "__main__":

    if len(sys.argv) != 1:
        raise Exception("extraneous arguments")

    os.system('cls' if os.name == 'nt' else 'clear')

    print('''
    ====================================
        Lunar (Neural-Network Aimbot)
    ====================================
    ''')

    AIMBOT_STR = colored("ENABLED", 'green')
    update_output = lambda AIMBOT_STR: f"[!] AIMBOT IS [{AIMBOT_STR}]"

    main()


    #print(update_output(AIMBOT_STR), end='\r')

    #keyboard_listener()
