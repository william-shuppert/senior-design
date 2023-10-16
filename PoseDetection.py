import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the PoseNet model
model = tf.keras.models.load_model('path_to_posenet_model')

@app.route('/detect-pose', methods=['POST'])
def detect_pose():
    try:
        # Get image from POST request
        img_data = request.files['image'].read()
        np_img = np.fromstring(img_data, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Preprocess the image for PoseNet model
        input_img = cv2.resize(img, (224, 224))
        input_img = np.expand_dims(input_img, axis=0)
        input_img = input_img.astype('float32') / 255

        # Predict
        poses = model.predict(input_img)

        # Process and return the results
        # (In this example, we're simplifying the output for demonstration purposes.)
        pose_data = {
            "nose": poses[0].tolist(),
            # ... extract other keypoints ...
        }
        return jsonify(pose_data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
