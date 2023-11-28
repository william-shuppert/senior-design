# hello_pytorch.py
#import torch

#print("PyTorch version:", torch.__version__)
#print("Hello, World!")
#from ultralytics import YOLO

#model = YOLO('yolov8m-pose.pt')

#results = model(source="Untitled2.mov", show=True, conf=0.3, save=True)
# hello_pytorch.py
#import torch
#import cv2  # Import OpenCV

#print("PyTorch version:", torch.__version__)
#print("Hello, World!")
from ultralytics import YOLO
import cv2
import torch

def process_video_with_pytorch(input_video_path, output_video_path):
    # Load the YOLO model
    model = YOLO('yolov8m-pose.pt')

    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Define the codec and create VideoWriter object to save the output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (640, 640))

    # Process each frame in the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to the expected input size of the model
        frame_resized = cv2.resize(frame, (640, 640))

        # Process the frame with the YOLO model
        results = model(frame_resized)

        # TODO: Add code here to handle the results, such as drawing bounding boxes or keypoints

        # Write the frame into the output file
        out.write(frame_resized)

    # Release everything when job is finished
    cap.release()
    out.release()

