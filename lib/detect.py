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
import d3dshot
from PIL import Image


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


class Detect:
    def __init__(self):
        screen = mss.mss()
        os.chdir("lib")
        self.half_screen_width = screen.monitors[1]["width"] / 2
        self.half_screen_height = screen.monitors[1]["height"] / 2

         #this controls the initial box width and height
        self.centered_box_constant = 200

        #You can change these offsets
        self.detection_box = (int(self.half_screen_width - self.centered_box_constant/2 + 110),  #this controls right away from crosshair
                              int(self.half_screen_height - self.centered_box_constant/2 - 110), #this controls height of box up
                              int(self.half_screen_width + self.centered_box_constant/2 + 150),  #width of the box
                              int(self.half_screen_height + self.centered_box_constant/2 + 110)) #this controls height of box down

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='weights/yolov5s6.pt', force_reload=True)
        self.model.to("cuda")
        self.model.conf = 0.4  # confidence threshold (0-1)
        self.model.iou = 0.45  # NMS IoU threshold (0-1)
        self.model.classes = [0] #only include the person class
        self.screen_capture = d3dshot.create(capture_output="numpy")
        self.screen_capture.capture(region = self.detection_box)
        time.sleep(1)

    def detect_screen(self):
        x = 0
        while True:
            frame = self.screen_capture.get_latest_frame()
            x += 1
            print(f"frame: {x}")
            results = self.model(frame)
            results.print()



    #This uses relative direct input since that is what Fortnite and other FPS games accept
    def move_crosshair(self, x, y):
        x = int(x - self.half_screen_width)
        y = int(y - self.half_screen_height)
        ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
        command = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))








if __name__ == "__main__": print("You are in the wrong directory and are running the wrong file; you must run lunar.py")
