# Lunar
Lunar is a neural network aimbot that uses real-time object detection accelerated with CUDA on Nvidia GPUs.

## About

Lunar can be modified to work with a variety of FPS games; however, it is currently configured for Fortnite. Besides being general purpose, the main advantage of using Lunar is that it is virtually undetectable by anti-cheat software (no memory is meddled with).

The basis of Lunar's player detection is the [YOLOv5](https://github.com/ultralytics/yolov5) architecture written in the PyTorch framework.

https://user-images.githubusercontent.com/45726273/120973172-982d4180-c73c-11eb-9c34-2f650ae81c43.mp4

## Installation

1. Install a version of [Python](https://www.python.org/downloads/) 3.8 or later.

2. Navigate to the root directory. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary dependencies.

```
pip install -r requirements.txt
```

## Usage
```           
python lunar.py
```
To update sensitivity settings:
```           
python lunar.py setup
```

## Required in-game settings:
- 1920 x 1080 resolution
- 75% HUD scale

## Future Updates
- Use TensorRT for faster inference
- Train a model to detect players better than the YOLOv5s person detection
- Explore combining real-time object detection with k-means pixel clustering
- Implement better player tracking with support for controller
- Make an easy-to-use GUI

## Contributing
Pull requests are welcome. If you have any suggestions, questions, or find any issues, please open an [issue](https://github.com/zeyad-mansour/Lunar/issues) and provide some detail.
If you find this project interesting or helpful, please star the repository.
