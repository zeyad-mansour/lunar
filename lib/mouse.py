import ctypes
import math
import time

import win32api
import scipy.interpolate
import numpy as np

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

#TODO: update this to work better
def move_crosshair(x=None, y=None, duration=0.1, config=None, scoped=False, **kwargs):

    #approximate offsets
    if not scoped:
        x = (x - 960)/(3 * config["xy_sens"])
        y = (y - 540)/(3 * config["xy_sens"])
    else:
        x = (x - 960)*(config["targeting_sens"]/115)
        y = (y - 540)*(config["targeting_sens"]/115)

    coordinates =  interpolate_coordinates(start_windows_coordinates=(0, 0), end_windows_coordinates=(x, y))
    for x, y in coordinates:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
        time.sleep(duration / len(coordinates))
    #print("DEBUG: Waiting for 0.5 seconds.")
    #time.sleep(0.5)

def interpolate_coordinates(start_windows_coordinates, end_windows_coordinates, steps=60):
    x_coordinates = [start_windows_coordinates[0], end_windows_coordinates[0]]
    y_coordinates = [start_windows_coordinates[1], end_windows_coordinates[1]]
    if x_coordinates[0] == x_coordinates[1]:
        x_coordinates[1] += 1
    if y_coordinates[0] == y_coordinates[1]:
        y_coordinates[1] += 1
    interpolation_func = scipy.interpolate.interp1d(x_coordinates, y_coordinates)
    intermediate_x_coordinates = np.linspace(start_windows_coordinates[0], end_windows_coordinates[0], steps + 1)[1:]
    coordinates = list(map(lambda x: (int(round(x)), int(interpolation_func(x))), intermediate_x_coordinates))
    return coordinates

def to_windows_coordinates(x=0, y=0):
    display_width = win32api.GetSystemMetrics(0)
    display_height = win32api.GetSystemMetrics(1)
    windows_x = (x * 65535) // display_width
    windows_y = (y * 65535) // display_height

    return windows_x, windows_y
