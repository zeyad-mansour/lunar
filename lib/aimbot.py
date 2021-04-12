import numpy as np
from termcolor import colored
import timeit
import _thread
import imutils
import time
import mss
import cv2
import os
import signal
import sys
import torch
import win32api
from ctypes import windll
import ctypes
import pyautogui


PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class Aimbot:
    def __init__(self):
        self.aimbot_status = colored("ENABLED", 'green')
        self.screen = mss.mss()
        os.chdir("lib")
        self.half_screen_width = self.screen.monitors[1]["width"] / 2
        self.half_screen_height = self.screen.monitors[1]["height"] / 2

        #this controls the initial box width and height of the Lunar Vision window
        self.centered_box_constant = 200

        #You can change these offsets
        self.detection_box = (int(self.half_screen_width - self.centered_box_constant/2 + 110),  #this controls right away from crosshair
                              int(self.half_screen_height - self.centered_box_constant/2 - 110), #this controls height of box up
                              int(self.half_screen_width + self.centered_box_constant/2 + 150),  #width of the box
                              int(self.half_screen_height + self.centered_box_constant/2 + 110)) #this controls height of box down
        print("[INFO] Loading the neural network model")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s6')
        if torch.cuda.is_available():
            print(colored("CUDA ACCELERATION [ENABLED]", "green"))
        else:
            print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE", "red"))
            print(colored("[!] Check your pytorch installation, else performance will be very poor", "red"))
        self.model.conf = 0.4  # confidence threshold (0-1)
        self.model.iou = 0.45  # NMS IoU threshold (0-1)
        self.model.classes = [0] #only include the person class
        time.sleep(1)
        print("\n[INFO] PRESS 'F1' TO TOGGLE AIMBOT\n[INFO] PRESS 'ESCAPE' TO QUIT")

    def update_status_aimbot(self):
        if self.aimbot_status == colored("ENABLED", 'green'):
            self.aimbot_status = colored("DISABLED", 'red')
        else:
            self.aimbot_status = colored("ENABLED", 'green')
        sys.stdout.write("\033[K")
        print(f"[!] AIMBOT IS [{self.aimbot_status}]", end = "\r")

    def start(self):
        print("[INFO] Beginning screen capture")

        Aimbot.update_status_aimbot(self)

        while True:
            last_time = time.time()

            frame = np.array(self.screen.grab(self.detection_box))


            results = self.model(frame)
            if len(results.xyxy[0]) != 0:
                #to be implemented



            cv2.putText(frame, f"FPS {1 // (time.time() - last_time)}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
            cv2.imshow('Lunar Vision', frame)

            if cv2.waitKey(1) & 0xFF == ord('0'):
                break


    #This uses relative direct input since that is what Fortnite and other FPS games accept
    def move_crosshair(self, x, y):
        x = int(x - self.half_screen_width)
        y = int(y - self.half_screen_height)
        ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
        command = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

    def clean_up(self):
        print("\n[INFO] ESCAPE WAS PRESSED. QUITTING...")
        self.screen.close()
        cv2.destroyAllWindows()
        os._exit(1)

if __name__ == "__main__": print("You are in the wrong directory and are running the wrong file; you must run lunar.py")
