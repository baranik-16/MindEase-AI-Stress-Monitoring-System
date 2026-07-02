import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "fer2013")   # <-- extracted folder
MODELS_DIR = os.path.join(BASE_DIR, "../models")
os.makedirs(MODELS_DIR, exist_ok=True)

train_dir = os.path.join(DATA_DIR, "train")
val_dir = os.path.join(DATA_DIR, "test")

if not os.path.exists(train_dir):
    raise FileNotFoundError(
        f"❌ FER-2013 dataset not found at {DATA_DIR}. "
        "Download it from Kaggle (msambare/fer2013) and unzip there."
    )

# Preprocess images
datagen = ImageDataGenerator(rescale=1.0 / 255)

train_gen = datagen.flow_from_directory(
    train_dir,
    target_size=(48, 48),
    color_mode="grayscale",
    batch_size=64,
    class_mode="categorical",
)

val_gen = datagen.flow_from_directory(
    val_dir,
    target_size=(48, 48),
    color_mode="grayscale",
    batch_size=64,
    class_mode="categorical",
)

# Build CNN
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(48, 48, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(7, activation="softmax"),
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
print("🚀 Training CNN model on FER-2013 ...")
model.fit(train_gen, epochs=25, validation_data=val_gen)

# Save model
model_path = os.path.abspath(os.path.join(MODELS_DIR, "cnn_emotion_model.h5"))
model.save(model_path)
print(f"✅ Model saved at {model_path}")
