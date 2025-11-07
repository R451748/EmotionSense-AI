import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import sys
sys.stdout.reconfigure(encoding='utf-8')

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import cv2
import torch
import tensorflow as tf
from deepface import DeepFace
from transformers import pipeline
from datetime import datetime

# ================================
# ⚙️ GPU / Environment Info
# ================================
if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    print(f"⚡ GPU Detected: {device_name}")
else:
    print("⚠️ No GPU detected — running on CPU.")

tf.get_logger().setLevel('ERROR')


# ================================
# 🎭 Helper: Emoji Mapping
# ================================
def emotion_to_emoji(emotion):
    mapping = {
        "happy": "😄", "joy": "😄",
        "sad": "😢", "sadness": "😢",
        "angry": "😡", "anger": "😡",
        "fear": "😨", "disgust": "🤢",
        "surprise": "😲", "neutral": "😐",
        "calm": "😌"
    }
    return mapping.get(emotion.lower(), "🙂")


# ================================
# 💬 TEXT EMOTION DETECTION
# ================================
print("🧠 Loading text emotion model (DistilRoBERTa)...")
text_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def analyze_text(text):
    try:
        result = text_classifier(text)[0]
        emotion = result["label"]
        confidence = round(float(result["score"]) * 100, 2)
        emoji = emotion_to_emoji(emotion)

        print("\n----------------------------------")
        print(f"💬 Text: {text}")
        print(f"🎭 Emotion: {emotion} {emoji}")
        print(f"📊 Confidence: {confidence}%")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("----------------------------------\n")

        return {
            "emotion": emotion.capitalize(),
            "confidence": confidence,
            "emoji": emoji,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"⚠️ Text emotion detection error: {e}")
        return {"error": str(e), "confidence": 0, "emoji": "❌"}


# ================================
# 🎥 REAL-TIME CAMERA EMOTION DETECTION
# ================================
def live_camera_emotion():
    print("\n🎥 Starting EmotionSense AI — Real-Time Detection")
    print("📡 Press 'q' to quit.\n")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Error: Could not access camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame capture failed.")
            break

        try:
            results = DeepFace.analyze(
                img_path=frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )

            if not isinstance(results, list):
                results = [results]

            for res in results:
                dominant_emotion = res.get("dominant_emotion", "Unknown").capitalize()
                confidence = round(max(res.get("emotion", {}).values(), default=0), 2)
                emoji = emotion_to_emoji(dominant_emotion)
                region = res.get("region", {})

                x, y, w, h = (
                    region.get("x", 0),
                    region.get("y", 0),
                    region.get("w", 0),
                    region.get("h", 0),
                )

                # Draw bounding box and label
                if w > 0 and h > 0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

                label = f"{dominant_emotion} {emoji} ({confidence}%)"
                cv2.putText(
                    frame, label, (x, y - 10 if y > 20 else y + 20),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2,
                )

        except Exception as e:
            cv2.putText(
                frame, f"Detecting... {str(e)[:30]}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
            )

        # Header overlay
        header = "🖤 EmotionSense AI — Live Facial Emotion Detection"
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
        cv2.putText(
            frame, header, (20, 30),
            cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 1,
        )

        cv2.imshow("🖤 EmotionSense AI", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ EmotionSense AI stopped successfully.\n")


# ================================
# 🚀 CLI ENTRY POINT
# ================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n⚠️ Usage:")
        print("   python emotion_inference.py camera   # Live facial detection")
        print("   python emotion_inference.py \"I am happy today!\"   # Text detection\n")
        sys.exit(0)

    arg = sys.argv[1].lower()

    if arg == "camera":
        live_camera_emotion()
    else:
        text = " ".join(sys.argv[1:])
        analyze_text(text)
