import joblib
import numpy as np
import sqlite3
import os
import re

# Paths
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Load models safely
xgb_model = joblib.load(os.path.join(MODELS_DIR, "stress_xgb_model.pkl"))
text_model = joblib.load(os.path.join(MODELS_DIR, "text_stress_model.pkl"))
vectorizer = joblib.load(os.path.join(MODELS_DIR, "text_vectorizer.pkl"))

# ---------------------------------------------------------
# Feature extractors
# ---------------------------------------------------------
def extract_numeric_features(emotion: str, text: str):
    emotion_dict = {
        "angry": 2, "sad": 3, "fear": 5, "happy": 0,
        "neutral": 1, "surprise": 4, "disgust": 6
    }
    emotion_val = emotion_dict.get(emotion.lower(), 1)
    text = text or ""
    length = len(text)
    exclam = text.count("!")
    capital = sum(1 for c in text if c.isupper())
    return np.array([[emotion_val, length, exclam, capital]])

# ---------------------------------------------------------
# Suggestion logic
# ---------------------------------------------------------
def get_suggestions(stress_level, emotion=None):
    suggestions = {
        "Low": [
            "Maintain your calm mindset with light exercise or reading.",
            "Keep journaling gratitude to reinforce positive mood.",
            "Share your good energy—help someone else today."
        ],
        "Medium": [
            "Try 5 min box-breathing or short walk outside.",
            "Reduce screen time for an hour and stretch your body.",
            "Plan tomorrow early to reduce mental load."
        ],
        "High": [
            "Pause everything and take 10 deep breaths.",
            "Step away from work; call a supportive friend.",
            "Use a mindfulness app (Headspace, Calm) for guided relief."
        ]
    }

    # Emotion-aware nuance
    if emotion == "sad":
        suggestions["High"].append("Listen to calm, uplifting music—avoid sad playlists.")
    elif emotion == "angry":
        suggestions["High"].append("Do quick physical release: squeeze a ball, short jog.")
    elif emotion == "fear":
        suggestions["Medium"].append("Write down the fear and one small action you can take.")

    return suggestions.get(stress_level, ["Keep a balanced day."])

# ---------------------------------------------------------
# Main prediction function
# ---------------------------------------------------------
def predict_stress(emotion: str, text: str, username: str):
    try:
        # Decide which model(s) to use
        has_text = bool(text.strip())
        has_emotion = bool(emotion.strip())

        if has_text and has_emotion:
            # Combine predictions
            numeric_feats = extract_numeric_features(emotion, text)
            xgb_pred = xgb_model.predict_proba(numeric_feats)[0]
            xgb_stress = np.argmax(xgb_pred)

            text_vec = vectorizer.transform([text])
            text_pred = text_model.predict_proba(text_vec)[0]
            text_stress = np.argmax(text_pred)

            # Average both predictions
            combined = (xgb_pred + text_pred) / 2
            stress_index = np.argmax(combined)
            confidence = round(float(np.max(combined)), 2)
        elif has_text:
            text_vec = vectorizer.transform([text])
            pred_proba = text_model.predict_proba(text_vec)[0]
            stress_index = np.argmax(pred_proba)
            confidence = round(float(np.max(pred_proba)), 2)
        else:
            feats = extract_numeric_features(emotion, "")
            pred_proba = xgb_model.predict_proba(feats)[0]
            stress_index = np.argmax(pred_proba)
            confidence = round(float(np.max(pred_proba)), 2)

        stress_label = ["Low", "Medium", "High"][stress_index]
        suggestions = get_suggestions(stress_label)

        # Save to DB
        conn = sqlite3.connect(os.path.join(BASE_DIR, "user_data.db"))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (username, emotion, text_input, stress_level, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (username, emotion, text, stress_label, confidence))
        conn.commit()
        conn.close()

        return {
            "predicted_stress_level": stress_label,
            "confidence": confidence,
            "suggestions": suggestions
        }

    except Exception as e:
        print("❌ Error in predict_stress:", e)
        return {"error": str(e)}
