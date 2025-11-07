import librosa
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# 🎧 Path to your dataset
DATA_PATH = r"C:\Users\rohan\Desktop\EmotionSense\emotion-service\datasets\ravdess-emotional-speech-audio"

# 🎭 Emotion labels (based on RAVDESS numbering)
EMOTIONS = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfccs_scaled = np.mean(mfccs.T, axis=0)
        return mfccs_scaled
    except Exception as e:
        print(f"⚠️ Could not process {file_path}: {e}")
        return None

def load_data():
    X, Y = [], []
    for actor_folder in os.listdir(DATA_PATH):
        actor_path = os.path.join(DATA_PATH, actor_folder)
        if not os.path.isdir(actor_path):
            continue
        for file in os.listdir(actor_path):
            if not file.endswith(".wav"):
                continue
            # Extract emotion label from file name (positions 6–8)
            emotion_code = file.split("-")[2]
            emotion = EMOTIONS.get(emotion_code)
            if not emotion:
                continue
            feature = extract_features(os.path.join(actor_path, file))
            if feature is not None:
                X.append(feature)
                Y.append(list(EMOTIONS.keys()).index(emotion_code))
    return np.array(X), tf.keras.utils.to_categorical(Y, num_classes=len(EMOTIONS))

def build_voice_emotion_model(input_shape):
    model = Sequential([
        Dense(256, activation='relu', input_shape=(input_shape,)),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(len(EMOTIONS), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_voice_model():
    X, Y = load_data()
    print("✅ Loaded Data:", X.shape, Y.shape)
    model = build_voice_emotion_model(X.shape[1])
    model.fit(X, Y, epochs=50, batch_size=32, validation_split=0.2)
    model.save(r"C:\Users\rohan\Desktop\EmotionSense\emotion-service\models\voice_emotion_model.h5")
    print("🎉 Voice Emotion Model Trained & Saved!")

if __name__ == "__main__":
    train_voice_model()
