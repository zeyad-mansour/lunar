import ctypes
import cv2
import json
import math
import mss
import numpy as np
import os
import scipy.interpolate
import sys
import threading
import time
import torch
import win32api
from termcolor import colored


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
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Aimbot:
    def __init__(self):
        self.aimbot_status = colored("ENABLED", 'green')
        self.screen = mss.mss()
        self.half_screen_width = 960
        self.half_screen_height = 540

        #this controls the initial box width and height of the "Lunar Vision" window
        #you can modify this to change how large you want the detection area to be
        self.centered_box_constant = 200 #values larger than 215 will cause error (your own player will be aimed at)

        #You can change these offsets
        self.detection_box = (int(self.half_screen_width - self.centered_box_constant),  #x1 coord
                              int(self.half_screen_height - self.centered_box_constant), #y1 coord
                              int(self.half_screen_width + self.centered_box_constant),  #x2 coord
                              int(self.half_screen_height + self.centered_box_constant)) #y2 coord
        print("[INFO] Loading the neural network model")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload = True)
        if torch.cuda.is_available():
            print(colored("CUDA ACCELERATION [ENABLED]", "green"))
        else:
            print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE", "red"))
            print(colored("[!] Check your PyTorch installation, else performance will be poor", "red"))
        self.model.conf = 0.60   # confidence threshold (or base detection (0-1)
        self.model.iou = 0.45 # NMS IoU (0-1)
        self.model.classes = [0] #only include the person class
        self.current_detection = None
        self.mouse_delay = 0.05
        with open("config/config.json") as f:
            self.sens_config = json.load(f)
        print("\n[INFO] PRESS 'F1' TO TOGGLE AIMBOT\n[INFO] PRESS 'F2' TO QUIT")


    def update_status_aimbot(self):
        if self.aimbot_status == colored("ENABLED", 'green'):
            self.aimbot_status = colored("DISABLED", 'red')
        else:
            self.aimbot_status = colored("ENABLED", 'green')
        sys.stdout.write("\033[K")
        print(f"[!] AIMBOT IS [{self.aimbot_status}]", end = "\r")


    def sleep(duration, get_now=time.perf_counter):
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()


    def move_crosshair(self):
        x, y, targeted = self.current_detection
        if not targeted:
            scale_frac, scale_int = self.sens_config["xy_scale"]
        else:
            scale_frac, scale_int = self.sens_config["targeting_scale"]

        #this extends (repeats) the list based on the scaling calculated from the sensitivity settings
        coordinates = Aimbot.interpolate_coordinates_from_center((x, y))
        if scale_int == 0.0:
            coordinates = coordinates[:int((len(coordinates) - 1) * scale_frac)]
        else:
            float_index = int((len(coordinates) - 1) * scale_frac)
            coordinates *= int(scale_int)
            coordinates.extend(coordinates[:float_index])

        for x, y in coordinates:
            if self.current_detection[2] != targeted: return
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
            Aimbot.sleep(self.mouse_delay/len(coordinates)) #custom function since time.sleep is not accurate enough.
        #print("DEBUG: sleeping for 2 seconds")
        #time.sleep(2)

    #TODO: make this more efficient for lower sensitivities
    def interpolate_coordinates_from_center(absolute_coordinates):
        diff_x = absolute_coordinates[0] - 960
        diff_y = absolute_coordinates[1] - 540
        length = int(math.sqrt((diff_x)**2 + (diff_y)**2))
        if length == 0: return [(0, 0)]
        unit_x = diff_x/length
        unit_y = diff_y/length
        coord_list = [(0, 0)]
        sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += coord_list[k][0]
            sum_y += coord_list[k][1]
            coord_list.append((round(unit_x * k - sum_x), round(unit_y * k - sum_y)))
        coord_list.remove((0, 0))
        coord_list.remove((0, 0))
        return coord_list


    def start(self):
        print("[INFO] Beginning screen capture")
        Aimbot.update_status_aimbot(self)
        while True:
            last_time = time.perf_counter()
            frame = np.array(self.screen.grab(self.detection_box))
            results = self.model(frame)
            if len(results.xyxy[0]) != 0: #player detected
                first_pass = True
                for *box, conf, cls in results.xyxy[0]: #iterate over each person detected
                    x1y1 = [int(x.item()) for x in box[:2]]
                    x2y2 = [int(x.item()) for x in box[2:]]
                    cv2.rectangle(frame, x1y1, x2y2, (0, 0, 255), 2) #draw the bounding boxes for all of the player detections
                    cv2.putText(frame, f"{int(conf * 100)}%", x1y1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) #draw the confidence labels on the bounding boxes

                    # object detections are automatically ordered from greatest to least confidence
                    # best detection variables are assigned only once at the beginning of the loop
                    if first_pass and x1y1[0] > 10: #ensures that your own player is not aimed at
                        first_pass = False
                        x1, y1, x2, y2, best_conf = *x1y1, *x2y2, conf.item()
                        height = y2 - y1
                        relative_head_X, relative_head_Y = int((x1 + x2)/2), int((y1 + y2)/2 - height/2.5) #offset to roughly approximate the head using a ratio of the height
                        cv2.circle(frame, (relative_head_X, relative_head_Y), 5, (0, 255, 0), -1)
                        absolute_head_X, absolute_head_Y = relative_head_X + self.detection_box[0], relative_head_Y + self.detection_box[1]
                        targeted = True if win32api.GetKeyState(0x02) in (-127, -128) else False #checks if right mouse button is being held down
                        self.current_detection = (absolute_head_X, absolute_head_Y, targeted)
                        #pixel val is specific to 1920x1080 resolution at 75% HUD
                        if self.aimbot_status == colored("ENABLED", 'green') and ctypes.windll.gdi32.GetPixel(ctypes.windll.user32.GetDC(0), 1563, 953) != 16777215:
                            Aimbot.move_crosshair(self)
            else:
                self.current_detection = None
            cv2.putText(frame, f"FPS: {int(1/(time.perf_counter() - last_time))}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Lunar Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord('0'):
                break


    def clean_up(self):
        print("\n[INFO] F2 WAS PRESSED. QUITTING...")
        cv2.destroyAllWindows()
        self.screen.close()
        os._exit(1)

if __name__ == "__main__": print("You are in the wrong directory and are running the wrong file; you must run lunar.py")
