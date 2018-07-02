# Indoor-Tracker (in development...)

## Intro: 

### What the Indoor-Tracker suppose to do:
    The Indoor-Tracker will be a indoor-path-recording-application implemented with python. 
    The input will be several camera video streams located around a conference hall.
    During registration, a 128-dim face feature map will be collected using dlib-face-recognition from each visitor.
    A YOLO-based body tracking will be applied to the video streams to take down the trace of each visitor. Each trace without
    identification will be stored as temporary data. Whenever the camera got a clear shot of a face of a visitor, the face data 
    will be analyzed and matched with the dataset collected during the registration to identify the owner of that trace. 
    Once identified, the trace will be added to the record of that specific visitor.
    
### Something important to know:
    The Indoor-Tracker is still under development, and it heavily depends on other opensource frameworks and projects.
    Currently it is based on deep_sort_yolov3, which can be found at: 
        https://github.com/Qidian213/deep_sort_yolov3
        
    For dlib-face-recognition, download the model from:
        http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2\n
        http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
        
    Only modified and added files are provided due to copyright issues.


## Before you download it, check these out:
    This module contains:
        1. mnistAppBasicLinear.py: Basic simplified algorithm for training and utilizing the MNIST dataset.   
        2. mnistAppBetterCNN.py: Better implementation of a Convolutional-Neural-Network designed for training and utilizing the MNIST dataset.     
        3. mnistFunc.py: Graphic and algorithm supports to the above implementations.


