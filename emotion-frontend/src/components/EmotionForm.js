import React, { useState } from "react";
import { detectEmotion } from "../api";
import { Spinner } from "react-bootstrap";

export default function EmotionForm({ onResult }) {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (text.trim()) formData.append("text", text);

    try {
      const res = await detectEmotion(formData);
      onResult(res.data);
    } catch {
      alert("❌ Unable to connect to backend. Ensure Flask is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card bg-black text-warning p-4 border-0 shadow-lg rounded-4">
      <h3 className="text-center mb-3 fw-bold text-warning">
        ⚡ Emotion Detector
      </h3>

      <form onSubmit={handleSubmit}>
        <textarea
          className="form-control bg-dark text-light border-secondary mb-3"
          rows="3"
          placeholder="Type your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>

        <div className="border border-secondary rounded-3 p-3 text-center mb-3">
          <p className="small mb-2 text-light">
            Upload Image 🎭 or Audio 🎙️ (optional)
          </p>
          <input
            type="file"
            accept="image/*,audio/*"
            className="form-control bg-dark text-warning"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-warning w-100 fw-bold py-2"
        >
          {loading ? (
            <>
              <Spinner animation="border" size="sm" className="me-2" />
              Detecting...
            </>
          ) : (
            "Analyze Emotion"
          )}
        </button>
      </form>
    </div>
  );
}
