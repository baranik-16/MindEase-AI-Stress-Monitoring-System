import requests

BASE_URL = "http://127.0.0.1:5000"

# Register user
res = requests.post(f"{BASE_URL}/register", json={"username": "testuser", "password": "mypassword"})
print("Register:", res.json())

# Login
res = requests.post(f"{BASE_URL}/login", json={"username": "testuser", "password": "mypassword"})
print("Login:", res.json())

# Predict from text
res = requests.post(f"{BASE_URL}/predict/text", json={"text": "I'm feeling overwhelmed and stressed."})
print("Text Prediction:", res.json())

# Predict from emotion
res = requests.post(f"{BASE_URL}/predict/emotion", json={"emotion": "angry"})
print("Emotion Prediction:", res.json())
