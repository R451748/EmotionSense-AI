import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import sys
sys.stdout.reconfigure(encoding='utf-8')

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import torch
import torchaudio
import cv2
from transformers import pipeline
from deepface import DeepFace
from datetime import datetime

# ================================
# 🔹 Helper: Emoji Mapping
# ================================
def emotion_to_emoji(emotion):
    mapping = {
        "happy": "😄", "joy": "😄", "happiness": "😄",
        "sad": "😢", "sadness": "😢",
        "angry": "😡", "anger": "😡",
        "fear": "😨", "disgust": "🤢",
        "surprise": "😲", "neutral": "😐",
        "calm": "😌"
    }
    return mapping.get(emotion.lower(), "🙂")

# ================================
# 💬 TEXT EMOTION
# ================================
def analyze_text(text):
    try:
        classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        result = classifier(text)[0]
        emotion = result["label"]
        confidence = round(float(result["score"]), 3)
        emoji = emotion_to_emoji(emotion)

        return {
            "emotion": emotion.capitalize(),
            "confidence": confidence,
            "emoji": emoji,
            "type": "text"
        }
    except Exception as e:
        return {"error": str(e), "type": "text", "confidence": 0, "emoji": "❌"}

# ================================
# 🎭 FACIAL EMOTION (Static Image)
# ================================
def analyze_image(image_path):
    try:
        if not os.path.exists(image_path):
            return {"error": "File not found", "type": "facial", "confidence": 0, "emoji": "❌"}

        img = cv2.imread(image_path)
        if img is None:
            return {"error": "Invalid image format", "type": "facial", "confidence": 0, "emoji": "❌"}

        # ✅ Run DeepFace
        analysis = DeepFace.analyze(img_path=img, actions=["emotion"], enforce_detection=False, silent=True)
        if not isinstance(analysis, list):
            analysis = [analysis]

        result = analysis[0]
        emotion = result["dominant_emotion"].capitalize()
        confidence = round(float(max(result["emotion"].values())) / 100, 3)
        emoji = emotion_to_emoji(emotion)

        return {
            "emotion": emotion,
            "confidence": confidence,
            "emoji": emoji,
            "type": "facial"
        }
    except Exception as e:
        print(f"⚠️ Facial detection error: {e}")
        return {"error": str(e), "type": "facial", "confidence": 0, "emoji": "❌"}

# ================================
# 🎥 FACIAL EMOTION (Webcam Live)
# ================================
def analyze_camera():
    print("\n🎥 Starting webcam for real-time emotion detection...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Unable to access webcam.")
        return {"error": "Camera not available", "confidence": 0, "emoji": "❌", "type": "facial"}

    print("📸 Press 'q' to capture and analyze frame.\n")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        cv2.imshow("EmotionSense - Press 'q' to capture", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            print("🖼 Capturing frame for analysis...")
            temp_path = "captured_frame.jpg"
            cv2.imwrite(temp_path, frame)
            cap.release()
            cv2.destroyAllWindows()

            result = analyze_image(temp_path)
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return result

    cap.release()
    cv2.destroyAllWindows()
    return {"error": "Camera closed", "confidence": 0, "emoji": "❌", "type": "facial"}

# ================================
# 🔊 VOICE EMOTION
# ================================
def analyze_audio(audio_path):
    try:
        from speechbrain.pretrained import EncoderClassifier
        classifier = EncoderClassifier.from_hparams(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP")
        signal, fs = torchaudio.load(audio_path)
        out_prob, score, index, text_lab = classifier.classify_batch(signal)

        emotion = text_lab[0]
        confidence = round(float(score[0]), 3)
        emoji = emotion_to_emoji(emotion)

        return {
            "emotion": emotion.capitalize(),
            "confidence": confidence,
            "emoji": emoji,
            "type": "voice"
        }
    except Exception as e:
        print(f"⚠️ Audio Model Error: {e}")
        return {"error": f"Audio Model Error: {e}", "confidence": 0, "emoji": "❌", "type": "voice"}

# ================================
# 🧠 MAIN — For CLI Testing
# ================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Usage: python emotion_inference.py [text | image_path | audio_path | camera]")
        sys.exit(0)

    input_data = sys.argv[1]
    print("\n🚀 EmotionSense AI — Inference Started\n" + "-" * 45)

    try:
        if input_data.lower() == "camera":
            result = analyze_camera()
        elif input_data.lower().endswith((".jpg", ".jpeg", ".png")):
            result = analyze_image(input_data)
        elif input_data.lower().endswith((".wav", ".mp3")):
            result = analyze_audio(input_data)
        else:
            result = analyze_text(input_data)

        # ✅ Print clean readable output
        print(f"🧠 Mode: {result['type'].capitalize()} Emotion")
        print(f"🎭 Detected Emotion: {result.get('emotion', 'Unknown')} {result.get('emoji', '❌')}")
        print(f"📊 Confidence: {(result.get('confidence', 0) * 100):.2f}%")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 45 + "\n✅ Analysis Complete!\n")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
