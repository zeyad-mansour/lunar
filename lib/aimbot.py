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
        self.centered_box_constant = 300

        #You can change these offsets
        self.detection_box = (int(self.half_screen_width - self.centered_box_constant/2 + 50),  #x coord
                              int(self.half_screen_height - self.centered_box_constant/2 - 50), #y coord
                              int(self.half_screen_width + self.centered_box_constant/2 ),  #width of the box
                              int(self.half_screen_height + self.centered_box_constant/2)) #height of the box
        print("[INFO] Loading the neural network model")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s6')
        if torch.cuda.is_available():
            print(colored("CUDA ACCELERATION [ENABLED]", "green"))
        else:
            print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE", "red"))
            print(colored("[!] Check your pytorch installation, else performance will be very poor", "red"))
        self.model.conf = 0.45  # confidence threshold (0-1)
        self.model.iou = 0.45  # NMS IoU threshold (0-1)
        self.model.classes = [0] #only include the person class
        time.sleep(1)
        print("\n[INFO] PRESS 'F1' TO TOGGLE AIMBOT\n[INFO] PRESS 'F2' TO QUIT")

    def update_status_aimbot(self):
        if self.aimbot_status == colored("ENABLED", 'green'):
            self.aimbot_status = colored("DISABLED", 'red')
        else:
            self.aimbot_status = colored("ENABLED", 'green')
        sys.stdout.write("\033[K")
        print(f"[!] AIMBOT IS [{self.aimbot_status}]", end = "\r")

    #This uses relative direct input since that is what Fortnite and other FPS games accept
    def move_crosshair(self, x, y):
        x = int(x - self.half_screen_width)
        y = int(y - self.half_screen_height)
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
        command = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

    def start(self):
        print("[INFO] Beginning screen capture")

        Aimbot.update_status_aimbot(self)

        while True:
            last_time = time.time()

            frame = np.array(self.screen.grab(self.detection_box))
            results = self.model(frame)

            if len(results.xyxy[0]) != 0: #person detected
                run = True
                for *box, conf, cls in results.xyxy[0]:
                    x1y1 = tuple(box[:2])
                    x2y2 = tuple(box[2:])
                    cv2.rectangle(frame, x1y1, x2y2, color=[255, 255, 255], thickness=2) #draw the bounding boxes
                    cv2.putText(frame, f"{int(conf * 100)}%", x1y1,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) #draw the confidence labels on the bounding boxes

                    # object detections are automatically ordered from greatest to least confidence
                    # best detection variables are assigned only once at the beginning of the loop
                    if run:
                        x1, y1, x2, y2, best_conf = x1y1[0].item(), x1y1[1].item(), x2y2[0].item(), x2y2[1].item(), conf.item()
                        run = False

                #get proper coordinates and move the mouse if aimbot enabled
                if self.aimbot_status == colored("ENABLED", 'green'):
                    height = y2 - y1
                    headX, headY = int((x1 + x2)/2), int((y1 + y2)/2 - height/3) #offset to roughly approximate the head using a ratio of the height

                    cv2.circle(frame, (headX, headY), 5, (0, 0, 255), -1)

                    absX, absY = headX + self.detection_box[0], headY + self.detection_box[1]
                    Aimbot.move_crosshair(self, absX, absY)


            cv2.putText(frame, f"FPS {1 // (time.time() - last_time)}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Lunar Vision", frame)

            if cv2.waitKey(1) & 0xFF == ord('0'):
                break


    def clean_up(self):
        print("\n[INFO] F2 WAS PRESSED. QUITTING...")
        self.screen.close()
        cv2.destroyAllWindows()
        os._exit(1)

if __name__ == "__main__": print("You are in the wrong directory and are running the wrong file; you must run lunar.py")
