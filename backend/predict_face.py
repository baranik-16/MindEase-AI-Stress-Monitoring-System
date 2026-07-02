import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
import io
from PIL import Image

cnn_model = load_model("models/cnn_emotion_model.h5")

emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

def predict_face_emotion(base64_image):
    try:
        # Decode image
        image_data = base64.b64decode(base64_image.split(",")[1])
        image = Image.open(io.BytesIO(image_data)).convert('L')
        image = image.resize((48, 48))
        img_array = np.array(image).reshape(1, 48, 48, 1) / 255.0

        # Predict emotion
        preds = cnn_model.predict(img_array)
        emotion = emotion_labels[np.argmax(preds)]
        confidence = float(np.max(preds))

        return {"emotion": emotion, "confidence": round(confidence, 2)}
    except Exception as e:
        print("Error in predict_face_emotion:", e)
        return {"error": str(e)}
