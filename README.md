# Object Detection with Python, Deep Learning, and OpenCV

Multi-object detection project using OpenCV for video capture and bounding box drawing and a Mobilenet SSD model trained on COCO dataset for object detection.
This project is a fork of an original repository, modified to count detections of specific objects.

# Configuration
In main.py, you can modify the following variables for detection and payload sending:
- endpoint: address to your web server
- interval: time in seconds of when to send the payload
- labels_record: dictionary (objects to detect and count) sent as json payload

The list of possible objects to detect (COCO classes) can be found in: 
https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/

# File description
- main.py: Main program to run for starting detection indefinitely or until pressing key "q".
- send_payload.py: Function for sending detections as json payloads in http post request.
- test_server.py: (Optional) script for creating a server in localhost and testing the post request.

# Instructions
Install peoject dependencies detailed in requirements.txt running the following command on your console inside project's folder:

```
pip install -r requirements.txt
```

# References
The original repository belongs to the tutorial: https://dontrepeatyourself.org/post/object-detection-with-python-deep-learning-and-opencv/
