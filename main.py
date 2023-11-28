#import streamlit as st
#import torch
#import os
#from app import process_video_with_pytorch

# Define the path to the 'storage' directory
#storage_dir = 'storage'
#os.makedirs(storage_dir, exist_ok=True)

# Create a file uploader widget to upload a video file
#uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov"])

#if uploaded_file is not None:
    # Save the uploaded video to a path
#    uploaded_file_path = os.path.join(storage_dir, uploaded_file.name)
#    with open(uploaded_file_path, "wb") as f:
#        f.write(uploaded_file.getbuffer())
#    st.success("File uploaded successfully!")

    # Process the video file using PyTorch and save the output
 #   processed_file_path = your_pytorch_processing_function(uploaded_file_path)

    # Display the processed video file path or provide a download link in Streamlit
  #  st.write(f"The processed video is saved at: {processed_file_path}")
  #  with open(processed_file_path, "rb") as file:
  #      btn = st.download_button(
  #          label="Download Processed Video",
  #          data=file,
  #          file_name=os.path.basename(processed_file_path),
  #          mime="video/mp4"
  #      )
import streamlit as st
import os
from app import process_video_with_pytorch

# Define the path to the 'storage' directory
storage_dir = 'storage'
processed_storage_dir = 'processed_storage'
os.makedirs(storage_dir, exist_ok=True)
os.makedirs(processed_storage_dir, exist_ok=True)

# Create a file uploader widget to upload a video file
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov"])

if uploaded_file is not None:
    # Save the uploaded video to a path
    uploaded_file_path = os.path.join(storage_dir, uploaded_file.name)
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

    # Define the output path for the processed video
    processed_file_path = os.path.join(processed_storage_dir, 'processed_' + uploaded_file.name)

    # Process the video file using PyTorch and save the output
    process_video_with_pytorch(uploaded_file_path, processed_file_path)

    # Display the processed video file path or provide a download link in Streamlit
    st.write(f"The processed video is saved at: {processed_file_path}")
    with open(processed_file_path, "rb") as file:
        btn = st.download_button(
            label="Download Processed Video",
            data=file,
            file_name=os.path.basename(processed_file_path),
            mime="video/mp4"
        )
#col1, col2 = st.columns(2)

# Display the first video in the first column
#with col1:
    #st.header("Original Video")
    #st.video(uploaded_file)

# Display the second video in the second column
#with col2:
    #st.header("Processed Video")
    #st.video(processed_file_path)

