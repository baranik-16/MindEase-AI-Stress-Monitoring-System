import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from datasets import load_dataset

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../models")
os.makedirs(MODELS_DIR, exist_ok=True)

print("📥 Loading 'emotion' dataset from HuggingFace...")
dataset = load_dataset("emotion")

# Combine train + validation + test
df_train = pd.DataFrame(dataset["train"])
df_val = pd.DataFrame(dataset["validation"])
df_test = pd.DataFrame(dataset["test"])
df = pd.concat([df_train, df_val, df_test])

print(f"✅ Dataset loaded: {df.shape[0]} samples")

# Map emotion → stress level
def map_stress(e):
    if e in ["anger", "fear"]:
        return "High"
    elif e == "sadness":
        return "Medium"
    else:
        return "Low"

df["stress_label"] = df["label"].map(lambda i: map_stress(dataset["train"].features["label"].int2str(i)))

# Split
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["stress_label"], test_size=0.2, random_state=42
)

# TF-IDF
vectorizer = TfidfVectorizer(max_features=8000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Gradient Boosting model
print("🚀 Training text-based stress model...")
model = GradientBoostingClassifier()
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print(f"\n📊 Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred))

# Save model + vectorizer
model_path = os.path.abspath(os.path.join(MODELS_DIR, "text_stress_model.pkl"))
vect_path = os.path.abspath(os.path.join(MODELS_DIR, "text_vectorizer.pkl"))

joblib.dump(model, model_path)
joblib.dump(vectorizer, vect_path)
print(f"✅ Saved model to {model_path}")
print(f"✅ Saved vectorizer to {vect_path}")
