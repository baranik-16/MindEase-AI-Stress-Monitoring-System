from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import init_db, register_user, login_user
from predict_stress import predict_stress
from predict_face import predict_face_emotion
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import base64
import cv2
import os

app = Flask(__name__)
CORS(app)

# ✅ Initialize SQLite DB
init_db()

# ✅ Allow TensorFlow GPU memory growth (prevents crash)
physical_devices = tf.config.list_physical_devices('GPU')
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)

# ✅ Load CNN model (face emotion recognition)
CNN_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "cnn_emotion_model.h5")
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
cnn_model = None

if os.path.exists(CNN_MODEL_PATH):
    cnn_model = load_model(CNN_MODEL_PATH)
    print(f"✅ Loaded emotion CNN model: {CNN_MODEL_PATH}")
else:
    print("⚠️ CNN model not found — Webcam emotion input will be unavailable.")

# =====================================================================================
# --------------------------- AUTHENTICATION ROUTES -----------------------------------
# =====================================================================================

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'status': 'fail', 'message': 'Username and password are required'}), 400

    ok, msg = register_user(username, password)
    if ok:
        return jsonify({'status': 'success', 'message': 'User registered successfully'}), 200
    return jsonify({'status': 'fail', 'message': msg}), 409


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'status': 'fail', 'message': 'Username and password are required'}), 400

    if login_user(username, password):
        return jsonify({'status': 'success', 'message': 'Login successful', 'username': username}), 200
    return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

# =====================================================================================
# ---------------------------- STRESS PREDICTION --------------------------------------
# =====================================================================================

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    emotion = data.get('emotion', '').strip()
    text = data.get('text', '').strip()
    username = data.get('username', '').strip()

    if not (emotion or text):
        return jsonify({'status': 'fail', 'message': 'Provide emotion, text, or both'}), 400

    result = predict_stress(emotion, text, username)
    # Ensure suggestions always exist to prevent frontend .map() errors
    if "suggestions" not in result:
        result["suggestions"] = [
            "Take a short walk.",
            "Hydrate and take deep breaths.",
            "Keep a balanced routine."
        ]
    return jsonify(result), 200


# =====================================================================================
# --------------------------- FACE EMOTION PREDICTION ---------------------------------
# =====================================================================================

@app.route('/predict_face', methods=['POST'])
def predict_face():
    """Receives base64 webcam image and returns predicted emotion."""
    if cnn_model is None:
        return jsonify({"error": "CNN model not loaded"}), 500

    try:
        data = request.get_json(silent=True) or {}
        image_b64 = data.get("image")

        if not image_b64:
            return jsonify({"error": "No image received"}), 400

        # Decode and preprocess
        img_bytes = base64.b64decode(image_b64.split(",")[1])
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (48, 48))
        img = np.expand_dims(img, axis=[0, -1]) / 255.0

        preds = cnn_model.predict(img)
        emotion_label = EMOTION_LABELS[int(np.argmax(preds))]
        confidence = round(float(np.max(preds)), 2)

        print(f"🧠 Predicted emotion: {emotion_label} (conf: {confidence})")

        return jsonify({
            "emotion": emotion_label,
            "confidence": confidence
        })

    except Exception as e:
        print("❌ Face prediction error:", e)
        return jsonify({"error": str(e)}), 500


# =====================================================================================
# ----------------------------- ROOT CHECK --------------------------------------------
# =====================================================================================

@app.route('/')
def home():
    return jsonify({"message": "MindEase Backend API Running ✅"}), 200


# =====================================================================================
# ----------------------------- APP LAUNCH --------------------------------------------
# =====================================================================================

if __name__ == '__main__':
    print("🚀 Starting MindEase Backend...")
    app.run(debug=True)
