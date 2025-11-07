import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from datetime import datetime
import cv2
from deepface import DeepFace
from models.emotion_inference import analyze_text, analyze_audio, emotion_to_emoji

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Allow React frontend access


# ================================
# 🏠 HOME ROUTE
# ================================
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "✅ EmotionSense AI Backend Running 🚀",
        "endpoints": {
            "text": "/predict/text",
            "facial": "/predict/facial",
            "voice": "/predict/voice",
            "camera": "/camera"
        }
    })


# ================================
# 💬 TEXT EMOTION DETECTION
# ================================
@app.route('/predict/text', methods=['POST'])
def predict_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': '❌ No text provided'}), 400

        text = data['text']
        result = analyze_text(text)
        result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[TEXT] '{text}' ➡ {result['emotion']} ({result['confidence']*100:.2f}%)")
        return jsonify(result)
    except Exception as e:
        print(f"⚠️ Error in /predict/text: {e}")
        return jsonify({'error': str(e)}), 500


# ================================
# 🎭 FACIAL EMOTION DETECTION (UPLOAD / CAPTURE)
# ================================
@app.route('/predict/facial', methods=['POST'])
def predict_facial():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '❌ No image provided'}), 400

        file = request.files['file']
        path = "temp_image.jpg"
        file.save(path)

        # ✅ Verify valid file
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return jsonify({'error': '⚠️ Invalid or empty image file'}), 400

        # ✅ Read image properly
        img = cv2.imread(path)
        if img is None:
            os.remove(path)
            return jsonify({'error': '⚠️ Unable to read image'}), 400

        # ✅ DeepFace analysis
        try:
            analysis = DeepFace.analyze(
                img_path=img,
                actions=["emotion"],
                enforce_detection=False,
                silent=True
            )

            if not isinstance(analysis, list):
                analysis = [analysis]

            result = analysis[0]
            emotion = result["dominant_emotion"].capitalize()
            confidence = round(float(max(result["emotion"].values())) / 100, 3)
            emoji = emotion_to_emoji(emotion)

            final_result = {
                "emotion": emotion,
                "confidence": confidence,
                "emoji": emoji,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(f"[FACIAL] Emotion ➡ {emotion} ({confidence*100:.2f}%)")
            return jsonify(final_result)

        except Exception as deep_err:
            print(f"⚠️ DeepFace error: {deep_err}")
            return jsonify({'error': '⚠️ Could not detect emotion from face'}), 500

        finally:
            if os.path.exists(path):
                os.remove(path)

    except Exception as e:
        print(f"❌ Error in /predict/facial: {e}")
        return jsonify({'error': str(e)}), 500


# ================================
# 🎙️ VOICE EMOTION DETECTION
# ================================
@app.route('/predict/voice', methods=['POST'])
def predict_voice():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '❌ No audio file provided'}), 400

        file = request.files['file']
        path = "temp_audio.wav"
        file.save(path)

        result = analyze_audio(path)
        os.remove(path)

        result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[VOICE] Emotion ➡ {result['emotion']} ({result['confidence']*100:.2f}%)")

        return jsonify(result)
    except Exception as e:
        print(f"⚠️ Error in /predict/voice: {e}")
        return jsonify({'error': str(e)}), 500


# ================================
# 📸 LIVE CAMERA EMOTION STREAM
# ================================
def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not access camera.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)
            if not isinstance(result, list):
                result = [result]

            for res in result:
                emotion = res["dominant_emotion"].capitalize()
                emoji = emotion_to_emoji(emotion)
                region = res.get("region", {})
                x, y, w, h = region.get("x", 0), region.get("y", 0), region.get("w", 0), region.get("h", 0)

                if w > 0 and h > 0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(frame, f"{emotion} {emoji}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        except Exception:
            cv2.putText(frame, "Detecting...", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()


@app.route('/camera')
def camera_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# ================================
# 🚀 MAIN ENTRY POINT
# ================================
if __name__ == '__main__':
    print("\n🚀 EmotionSense AI Backend Starting...")
    print("🌐 Running on: http://localhost:5050")
    print("✅ Endpoints: /predict/text, /predict/facial, /predict/voice, /camera\n")

    app.run(host='0.0.0.0', port=5050, debug=False)
