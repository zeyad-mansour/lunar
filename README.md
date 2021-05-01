# Lunar 🌕
Lunar is a neural network aimbot that uses real-time object detection accelerated with CUDA on Nvidia GPUs.

Note: This project is very much under development, but right now, i'm putting it on the back burner due to other obligations that I have.

## About

Lunar can be modified to work with a variety of FPS games; however, it is currently configured for Fortnite. Besides being easy-to-use, the main benefit of Lunar is that it is virtually undetectable by anti-cheat software (no memory is meddled with).

The basis of Lunar's player detection is the [YOLOv5](https://github.com/ultralytics/yolov5) architecture written in the PyTorch framework

https://user-images.githubusercontent.com/45726273/116477665-eb14fe80-a84a-11eb-9a14-7b413d2933d7.mp4

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
- Use TensorRT for faster inference.
- Train a custom model to detect players better than the YOLOv5s person detection.
- Explore combining real-time object detection with k-means pixel clustering
- Implement smooth, natural player tracking (bezier curve)


## Contributing
If you have any suggestions or find any issues, please open an [issue](https://github.com/zeyad-mansour/Lunar/issues) and provide some detail.

If you'd like to contribute by donating, that would be much appreciated, and you can do that [here](https://www.zeyadmansour.com/info.txt) :) 
