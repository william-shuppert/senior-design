import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st



def process(video, server_url: str):
    files = {"file": ("filename", video, "video/mp4")}
    response = requests.post(server_url, files=files, stream=True)
    return response

def app(backend):    
    # construct UI layout
    st.title("Pose Detection Using MediaPipe")

    st.write("Track your pose below!")  # description and instructions

    input_file = st.file_uploader("Upload Video")

    if st.button("Analyze"):

        col1, col2 = st.columns(2)

        if input_file:
            res = process(input_file, backend + "/pose-detection")
            col1.header("Original")
            col1.video(input_file)

            video_path = res.json()
            col2.header("Tracked")
            col2.video(video_path.get("name"))
        else:
            # handle case with no image
            st.write("Please Upload a File!")