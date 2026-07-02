import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb

# ==============================================================
#  Setup paths
# ==============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../models")
os.makedirs(MODELS_DIR, exist_ok=True)

# ==============================================================
#  Load text-based dataset (Stress Tweets)
# ==============================================================
from datasets import load_dataset
print("📥 Loading tweet-eval stress dataset ...")
dataset = load_dataset("mrm8488/tweet-eval-stress")

train_df = pd.DataFrame(dataset["train"])
test_df = pd.DataFrame(dataset["test"])
df = pd.concat([train_df, test_df])

# Map labels: 0 = non-stress, 1 = stress
df = df.rename(columns={"label": "stress"})
df["stress_label"] = df["stress"].map({0: "Low", 1: "High"})
df = df.dropna(subset=["text"]).reset_index(drop=True)

# ==============================================================
#  Text preprocessing and feature extraction
# ==============================================================
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_tfidf = vectorizer.fit_transform(df["text"]).toarray()

# Add simple text metrics as numerical features
text_len = df["text"].apply(len)
exclam = df["text"].apply(lambda t: t.count("!"))
caps = df["text"].apply(lambda t: sum(1 for c in t if c.isupper()))
extra_features = np.vstack([text_len, exclam, caps]).T

# Combine TF-IDF and numeric features
X_full = np.hstack([X_tfidf, extra_features])
y = df["stress_label"]

# ==============================================================
#  Train-test split
# ==============================================================
X_train, X_test, y_train, y_test = train_test_split(X_full, y, test_size=0.2, random_state=42)

# ==============================================================
#  Train XGBoost model
# ==============================================================
print("🚀 Training improved XGBoost model ...")
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss",
    use_label_encoder=False
)
model.fit(X_train, y_train)

# ==============================================================
#  Evaluate
# ==============================================================
y_pred = model.predict(X_test)
print("\n📊 Model Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ==============================================================
#  Save model and vectorizer
# ==============================================================
model_path = os.path.abspath(os.path.join(MODELS_DIR, "stress_xgb_model.pkl"))
vectorizer_path = os.path.abspath(os.path.join(MODELS_DIR, "text_vectorizer.pkl"))

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print(f"✅ Saved improved XGBoost model to: {model_path}")
print(f"✅ Saved vectorizer to: {vectorizer_path}")
