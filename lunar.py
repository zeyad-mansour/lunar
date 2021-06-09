import argparse
import json
import msvcrt
import os
import sys
import threading

from lib.aimbot import Aimbot
from pynput import keyboard
from termcolor import colored
from math import modf


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
    os.chdir("lib")
    lunar = Aimbot()
    lunar.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    print("[INFO] In-game X and Y axis sensitivity should be the same")
    def prompt(str):
        valid_input = False
        while not valid_input:
            try:
                number = float(input(str))
                valid_input = True
            except ValueError:
                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")
        return number

    xy_sens = prompt("X-Axis and Y-Axis Sensitivity (from in-game settings): ")
    targeting_sens = prompt("Targeting Sensitivity (from in-game settings): ")

    print("[INFO] Your in-game targeting sensitivity must be the same as your scoping sensitivity")
    sensitivity_settings = {"xy_sens": xy_sens, "targeting_sens": targeting_sens, "xy_scale": 10/xy_sens, "targeting_scale": 1000/(targeting_sens * xy_sens)}

    with open('lib/config/config.json', 'w') as outfile:
        json.dump(sensitivity_settings, outfile)
    print("[INFO] Sensitivity configuration complete")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    print(colored('''
    | |
    | |    _   _ _ __   __ _ _ __
    | |   | | | | '_ \ / _` | '__|
    | |___| |_| | | | | (_| | |
    \_____/\__,_|_| |_|\__,_|_|

    (Neural-Network Aimbot)''', "yellow"))

    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup()
    elif not os.path.exists("lib/config/config.json"):
        print("[!] Sensitivity configuration is not set")
        setup()
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
