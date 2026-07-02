# MindEase – AI-Based Stress Monitoring System for Healthcare Workers

MindEase is a full-stack stress monitoring web application built to help healthcare workers check and track their stress levels using text input, facial emotion recognition, or both.

The project combines a React frontend, Flask backend, SQLite database, and machine learning models for text-based stress analysis and webcam-based facial emotion detection. Based on the predicted stress level, the application provides practical recommendations to help users manage stress during or after demanding work shifts.

---

## Overview

Healthcare workers often deal with long hours, emotional pressure, and high workloads. MindEase was developed as a simple digital tool that can quickly estimate stress levels without relying on lengthy questionnaires or external wearable devices.

The system supports three input modes:

- Text input
- Webcam-based facial emotion input
- Combined text and webcam input

The final output includes:

- Predicted stress level: Low, Medium, or High
- Confidence score
- Detected emotion
- Personalised stress-relief suggestions

---

## Features

- Secure user registration and login
- Text-based stress prediction
- Webcam-based facial emotion recognition
- Multiple input modes: Text, Webcam, or Both
- Real-time stress level prediction
- Stress-relief recommendations based on predicted level
- SQLite database for storing user and prediction records
- React dashboard with clean and simple UI
- Flask REST APIs for authentication, prediction, and emotion analysis

---

## Tech Stack

### Frontend
- React JS
- React Router
- Axios
- React Webcam
- CSS

### Backend
- Python
- Flask
- Flask-CORS
- SQLite
- OpenCV
- NumPy
- Joblib

### Machine Learning
- TensorFlow / Keras
- Scikit-learn
- XGBoost
- TF-IDF Vectorizer
- CNN for facial emotion recognition

---

## Machine Learning Approach

MindEase uses multiple models to support different types of input.

### 1. Text-Based Stress Detection

The text entered by the user is converted into numerical features using TF-IDF. These features are then passed into a machine learning classifier trained to identify stress-related patterns in text.

This model helps detect signs of stress such as anxiety, frustration, tiredness, pressure, or emotional fatigue.

### 2. Facial Emotion Recognition

For webcam input, the system captures an image from the user’s camera and sends it to the Flask backend. The image is resized, converted to grayscale, and passed into a CNN model trained on facial emotion data.

The CNN predicts emotions such as:

- Happy
- Sad
- Angry
- Fear
- Neutral
- Surprise
- Disgust

These emotions are then used as part of the stress prediction process.

### 3. Hybrid Prediction

When both text and webcam inputs are provided, the system combines the information from both sources to make a more balanced prediction.

This improves reliability because stress may be expressed through words, facial expressions, or both.

---

## Project Structure

```text
MindEase-AI-Stress-Monitoring-System/
│
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── predict_stress.py
│   ├── predict_face.py
│   ├── init_db.py
│   ├── requirements.txt
│   │
│   ├── train_models/
│   │   ├── train_text_model.py
│   │   ├── train_emotion_model.py
│   │   └── train_xgb_model.py
│   │
│   ├── models/
│   │   ├── cnn_emotion_model.h5
│   │   ├── text_stress_model.pkl
│   │   ├── text_vectorizer.pkl
│   │   └── stress_xgb_model.pkl
│   │
│   └── db/
│       └── users.db
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── Dashboard.js
│   │   ├── App.js
│   │   ├── api.js
│   │   └── index.js
│   │
│   ├── package.json
│   └── .env
│
├── .gitignore
└── README.md