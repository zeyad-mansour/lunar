import ctypes
import cv2
import json
import mss
import numpy as np
import os
import sys
import time
import torch
import win32api
from termcolor import colored
from lib.mouse import move_crosshair


class Aimbot:
    def __init__(self):
        self.aimbot_status = colored("ENABLED", 'green')
        self.screen = mss.mss()
        self.half_screen_width = 960
        self.half_screen_height = 540

        #this controls the initial box width and height of the "Lunar Vision" window
        #you can modify this to change how large you want the detection area to be
        self.centered_box_constant = 320

        #You can change these offsets
        self.detection_box = (int(self.half_screen_width - self.centered_box_constant/8),  #x1 coord
                              int(self.half_screen_height - self.centered_box_constant), #y1 coord
                              int(self.half_screen_width + self.centered_box_constant),  #x2 coord
                              int(self.half_screen_height + self.centered_box_constant)) #y2 coord
        print("[INFO] Loading the neural network model")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload = True)
        if torch.cuda.is_available():
            print(colored("CUDA ACCELERATION [ENABLED]", "green"))
        else:
            print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE", "red"))
            print(colored("[!] Check your pytorch installation, else performance will be very poor", "red"))

        self.model.conf = 0.35   # confidence threshold (or base detection (0-1)
        self.model.iou = 0.45 # NMS IoU (0-1)
        self.model.classes = [0] #only include the person class

        with open("config/config.json") as f:
            self.config = json.load(f)

        print("\n[INFO] PRESS 'F1' TO TOGGLE AIMBOT\n[INFO] PRESS 'F2' TO QUIT")

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
        dc = ctypes.windll.user32.GetDC(0)

        while True:
            last_time = time.perf_counter()

            frame = np.array(self.screen.grab(self.detection_box))
            cv2.rectangle(frame, (0, self.centered_box_constant), (self.centered_box_constant//8, self.centered_box_constant * 2), (0, 0, 0), -1) #draw box over own player
            results = self.model(frame)

            if len(results.xyxy[0]) != 0: #person detected
                first_pass = True
                for *box, conf, cls in results.xyxy[0]: #iterate over each person detected
                    x1y1 = [int(x.item()) for x in box[:2]]
                    x2y2 = [int(x.item()) for x in box[2:]]
                    cv2.rectangle(frame, x1y1, x2y2, (0, 0, 255), 2) #draw the bounding boxes
                    cv2.putText(frame, f"{int(conf * 100)}%", x1y1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) #draw the confidence labels on the bounding boxes

                    # object detections are automatically ordered from greatest to least confidence
                    # best detection variables are assigned only once at the beginning of the loop
                    if first_pass:
                        x1, y1, x2, y2, best_conf = *x1y1, *x2y2, conf.item()
                        first_pass = False

                height = y2 - y1

                relative_head_X, relative_head_Y = int((x1 + x2)/2), int((y1 + y2)/2 - height/2.5) #offset to roughly approximate the head using a ratio of the height

                cv2.circle(frame, (relative_head_X, relative_head_Y), 6, (0, 255, 0), -1)

                absolute_head_X, absolute_head_Y = relative_head_X + self.detection_box[0], relative_head_Y + self.detection_box[1]

                if self.aimbot_status == colored("ENABLED", 'green'):

                    #checks the pixel val to see if the pickaxe is not selected
                    #this pixel val is Fortnite specific to 1920x1080 resolution at 75% HUD; it would need to be modified for any other configuration
                    if ctypes.windll.gdi32.GetPixel(dc, 1563, 953) != 16777215: #checks the pixel val to see if the pickaxe is not selected
                        scoped = True if win32api.GetKeyState(0x02) in (-127, -128) else False #checks if right mouse button is down
                        move_crosshair(x = absolute_head_X, y = absolute_head_Y, duration = 0.01, config = self.config, scoped = scoped)

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
