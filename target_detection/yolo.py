import cv2
from pathlib import Path
import numpy as np


# This file depends on the yolo cfg, weights and class names
#
# git clone https://github.com/AlexeyAB/darknet.git
# wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
# And set path below

yolo_path=Path("/home/energycorp.com/u40420/projects/hackday/darknet/cfg")
# Load the pre-trained YOLOv3-tiny model
net = cv2.dnn.readNetFromDarknet(cv2.samples.findFile(str(yolo_path / "yolov4.cfg")),
                                  cv2.samples.findFile(str(yolo_path / "yolov4.weights")))
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def find_target(cap):
    return find_person(cap.frame)

def find_person(image):
    # Load the input image
 
    # Create a 4D blob from the input image
    blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), swapRB=True, crop=False)

    # Set the input blob for the network
    net.setInput(blob)

    # Get the names of the output layers
    output_layers = net.getLayerNames()
    print(output_layers)
    print(list(net.getUnconnectedOutLayers()))
    print("a")
    print([i for i in list(net.getUnconnectedOutLayers())])
    output_layers = [output_layers[i - 1] for i in net.getUnconnectedOutLayers()]

    # Run the forward pass to get the network output
    outputs = net.forward(output_layers)

    # Get the confidence threshold for the detections
    conf_threshold = 0.5

    # Get the class labels for the detections
    class_labels = []
    with open(str(yolo_path / "coco.names"), "r") as f:
        class_labels = [line.strip() for line in f.readlines()]

    # Loop over the detections and draw boxes around the objects
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                width = int(detection[2] * image.shape[1])
                height = int(detection[3] * image.shape[0])
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                cv2.rectangle(image, (left, top), (left + width, top + height), (0, 255, 0), 2)
                cv2.putText(image, f"{class_labels[class_id]} {confidence:.2f}", (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Show the output image
    cv2.imshow("Object detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return


if __name__ == "__main__":


    from djitellopy import Tello

    tello = Tello()
    tello.connect()
    tello.streamon()

    cap = tello.get_frame_read()

    while True:
        find_target(cap)
    
    cv2.destroyAllWindows()