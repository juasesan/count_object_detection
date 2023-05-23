import numpy as np
import cv2
import datetime

from send_payload import send_payload

# define the variables to send the data in post request
endpoint = 'http://localhost:8000'
interval = 60   # interval of time in seconds to send the data
# dictionary (objects to detect and count) sent as json payload
labels_record = {
    'BANANA': 0,
    'APPLE': 0,
    'BOTTLE': 0,
    'SPOON' : 0
}  

# set the camera to use
video_cap = cv2.VideoCapture(0)

# grab the width and the height of the video stream
frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_cap.get(cv2.CAP_PROP_FPS))

# path to the weights and model files
weights = "./ssd_mobilenet/frozen_inference_graph.pb"
model = "./ssd_mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

# load the MobileNet SSD model trained  on the COCO dataset
net = cv2.dnn.readNetFromTensorflow(weights, model)

# load the class labels the model was trained on
class_names = []
with open("./ssd_mobilenet/coco_names.txt", "r") as f:
    class_names = f.read().strip().split("\n")

# create a list of random colors to represent each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(class_names)+1, 3))


start_time = datetime.datetime.now()

# loop over the frames
while True:
    # take a capture of the video
    success, frame = video_cap.read()
    h = frame.shape[0]
    w = frame.shape[1]

    # create a blob from the frame
    blob = cv2.dnn.blobFromImage(
        frame, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
    # pass the blog through our network and get the output predictions
    net.setInput(blob)
    output = net.forward() # shape: (1, 1, 100, 7)

    # Check whether the interval to record the data was reached
    elapsed_time = datetime.datetime.now() - start_time
    recorder = True if int(elapsed_time.total_seconds()) >= interval else False

    # loop over the number of detected objects
    for detection in output[0, 0, :, :]: # output[0, 0, :, :] has a shape of: (100, 7)
        # the confidence of the model regarding the detected object
        probability = detection[2]
        # if the confidence of the model is lower than 50%,
        # we do nothing (continue looping)
        if probability < 0.5:
            continue

        # extract the ID of the detected object to get
        # its name and the color associated with it
        class_id = int(detection[1])
        label = class_names[class_id - 1].upper()
        color = colors[class_id]
        B, G, R = int(color[0]), int(color[1]), int(color[2])

        # record object count in a dictionary each minute
        if recorder and (label in labels_record):
            labels_record[label] += 1

        # perform element-wise multiplication to get
        # the (x, y) coordinates of the bounding box
        box = [int(a * b) for a, b in zip(detection[3:7], [w, h, w, h])]
        box = tuple(box)

        # draw the bounding box of the object
        cv2.rectangle(frame, box[:2], box[2:], (B, G, R), thickness=2)

        # draw the name of the predicted object along with the probability
        text = f"{label} {probability * 100:.2f}%"
        cv2.putText(frame, text, (box[0], box[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if recorder:
        print('Detected objects:')
        print(labels_record)
        print('Sending payload...')
        send_payload(endpoint, labels_record)

        # restart variables
        labels_record = {
            'BANANA': 0,
            'APPLE': 0,
            'BOTTLE': 0,
            'SPOON' : 0
        } 
        start_time = datetime.datetime.now()
        recorder = False

    cv2.imshow("Output", frame)
    
    if cv2.waitKey(10) == ord("q"):
        break

# release the video capture, video writer, and close all windows
video_cap.release()
cv2.destroyAllWindows()