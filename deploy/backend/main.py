import asyncio
import io
import imageio
from fastapi.responses import StreamingResponse
import mediapipe as mp
import time
import uuid
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import cv2
from requests import Response
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
import numpy as np
from PIL import Image

import config
import inference


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


async def combine_images(output, resized, name):
    final_image = np.hstack((output, resized))
    cv2.imwrite(name, final_image)


@app.post("/pose-detection")
async def get_video(file: UploadFile = File(...)):
    start = time.time()
    name = f"/storage/{str(uuid.uuid4())}.mp4"

    # Read the video content from the uploaded file
    video_content = await file.read()
    
    # Use io.BytesIO to create a file-like object from the bytes
    video_stream = io.BytesIO(video_content)

    # Get the reader for the video content
    reader = imageio.get_reader(video_stream, format="mp4")

    # Get frames and perform any desired processing
    processed_frames = []
    with mp.solutions.pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5) as pose:
        for frame in reader:
            results = pose.process(frame)

            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

            processed_frames.append(frame)

    # Use imageio.get_writer to write the processed frames to the BytesIO object
    with imageio.get_writer(name, fps=reader.get_meta_data()["fps"], format="FFMPEG") as writer:
        for frame in processed_frames:
            writer.append_data(frame)

    return {"name": name, "time": time.time() - start}


    ##### The following shows how you would return the video instead of saving it to the shared storage file #####


    # Create a BytesIO object to store the processed frames
    output_stream = io.BytesIO()

    # Use ffmpeg.get_writer to write the processed frames to the BytesIO object
    with imageio.get_writer(output_stream, fps=reader.get_meta_data()["fps"], format="mp4") as writer:
        for frame in processed_frames:
            writer.append_data(frame)

    # Reset the BytesIO stream to the beginning
    output_stream.seek(0)

    # Return the processed video as a streaming response
    return StreamingResponse(output_stream, media_type="video/mp4", headers={"Content-Disposition": "inline; filename=processed_video.mp4"})


@app.post("/{style}")
async def get_image(style: str, file: UploadFile = File(...)):
    image = np.array(Image.open(file.file))
    model = config.STYLES[style]
    start = time.time()
    output, resized = inference.inference(model, image)
    name = f"/storage/{str(uuid.uuid4())}.jpg"
    print(f"name: {name}")
    # name = file.file.filename
    cv2.imwrite(name, output)
    #models = config.STYLES.copy()
    #del models[style]
    #asyncio.create_task(generate_remaining_models(models, image, name))
    return {"name": name, "time": time.time() - start}


async def generate_remaining_models(models, image, name: str):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, name)
    )


def process_image(models, image, name: str):
    for model in models:
        output, resized = inference.inference(models[model], image)
        name = name.split(".")[0]
        name = f"{name.split('_')[0]}_{models[model]}.jpg"
        cv2.imwrite(name, output)

# **************************** Segmentation ************************
from segmentation_demo.segmentation import get_segmentator, get_segments
seg_model = get_segmentator()

@app.post("/segmentation/param")
async def get_segmentation_map(file: bytes = File(...)):
    """Get segmentation maps from image file"""
    segmented_image = get_segments(seg_model, file)
    bytes_io = io.BytesIO()
    segmented_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
