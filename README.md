# Lunar 🌕
Lunar is a neural network aimbot that uses real-time object detection accelerated with CUDA on Nvidia GPUs.

## About

Lunar can be modified to work with a variety of FPS games; however, it is currently configured for Fortnite. Besides being easy-to-use, the main benefit of Lunar is that it is virtually undetectable by anti-cheat software (no memory is meddled with).

The basis of Lunar's player detection is the [YOLOv5](https://github.com/ultralytics/yolov5) architecture written in the PyTorch framework.

## Installation

1. Install [Python](https://www.python.org/downloads/) 3.8 or later


2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary dependencies.

```
pip3 install -r requirements.txt
```

## Usage

```
python lunar.py
```
## Future Updates
- Train a custom model to detect players with a greater mAP than the YOLOv5s default person detection.
- Explore combining real-time object detection with pixel color tracking
- Implement smooth, natural player tracking (bezier curve)


## Contributing
If you have any suggestions or find any issues, please open an [issue](https://github.com/zeyad-mansour/Lunar/issues) and provide some detail.
