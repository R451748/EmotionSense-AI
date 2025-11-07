import React, { useState } from "react";
import { Container, Row, Col, Card, Button, Form, Spinner } from "react-bootstrap";
import { Camera, Type } from "react-bootstrap-icons";
import "bootstrap/dist/css/bootstrap.min.css";


export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [emotion, setEmotion] = useState(null);
  const [input, setInput] = useState("");
  const [showCamera, setShowCamera] = useState(false);


  const handleTextEmotion = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5050/predict/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });
      const data = await res.json();
      if (data && data.emotion) {
        data.timestamp = new Date().toISOString();
        setEmotion(data);
      } else {
        setEmotion({ error: "⚠️ No emotion detected." });
      }
    } catch (err) {
      console.error(err);
      setEmotion({ error: "❌ Unable to connect to backend." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-vh-100 bg-black text-light d-flex flex-column">
      {/* Navbar */}
      <nav className="navbar navbar-dark bg-black border-bottom border-warning shadow-sm py-3 px-4">
        <h4 className="fw-bold text-warning m-0 glow-text">
          <i className="bi bi-emoji-smile-fill me-2"></i> EmotionSense AI
        </h4>
        <Button variant="outline-warning" href="/" size="sm" className="fw-bold">
          Home
        </Button>
      </nav>

      {/* Main Dashboard */}
      <Container className="flex-grow-1 py-5">
        <h2 className="text-center text-warning fw-bold mb-5 animate-header">
          Analyze Emotions Instantly 🚀
        </h2>

        <Row className="g-4 justify-content-center">
          {/* TEXT EMOTION */}
          <Col md={4}>
            <Card className="bg-dark border border-warning shadow-lg rounded-4 p-3 h-100 hover-card">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <Type size={28} className="text-warning me-2" />
                  <h5 className="m-0 text-light">Text Emotion</h5>
                </div>

                <Form onSubmit={handleTextEmotion}>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Type your text here..."
                    className="bg-black text-light border-secondary mb-3"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                  />
                  <Button
                    variant="warning"
                    type="submit"
                    className="w-100 fw-bold py-2 glow-button"
                  >
                    {loading ? (
                      <>
                        <Spinner animation="border" size="sm" className="me-2" /> Analyzing...
                      </>
                    ) : (
                      "Analyze Text"
                    )}
                  </Button>
                </Form>

                {/* Result Display */}
                {emotion && !emotion.error && (
                  <div className="result-card text-center mt-4 p-3 rounded-4 border border-warning shadow-sm">
                    <h6 className="text-warning fw-bold mb-2">Detected Emotion</h6>
                    <h4 className="fw-bold text-uppercase mb-3 text-light animate-emoji">
                      {emotion.emotion} {emotion.emoji}
                    </h4>
                    <div className="progress mb-2 mx-auto" style={{ height: "6px", width: "80%" }}>
                      <div
                        className="progress-bar bg-warning"
                        role="progressbar"
                        style={{
                          width: `${(emotion.confidence || 0) * 100}%`,
                          transition: "width 0.8s ease-in-out",
                        }}
                      ></div>
                    </div>
                    <small className="text-muted d-block mt-2">
                      Confidence: {(emotion.confidence * 100).toFixed(2)}%
                    </small>
                    <small className="text-secondary d-block">
                      ⏰ {new Date(emotion.timestamp).toLocaleString()}
                    </small>
                  </div>
                )}

                {/* Error Display */}
                {emotion && emotion.error && (
                  <div className="alert alert-danger mt-4 text-center py-2">
                    {emotion.error}
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>

          {/* IMAGE EMOTION */}
          <Col md={4}>
            <Card className="bg-dark border border-warning shadow-lg rounded-4 p-3 h-100 text-center hover-card">
              <Card.Body>
                <Camera size={30} className="text-warning mb-3" />
                <h5 className="text-light">Facial Emotion</h5>
                <p className="text-secondary small">
                  Capture live emotion via your camera.
                </p>
                {/* CAMERA EMOTION (Embedded in same page) */}
<Button
  variant="warning"
  className="fw-bold w-100 glow-button"
  onClick={() => setShowCamera((prev) => !prev)}
>
  {showCamera ? "Close Camera" : "Open Camera"}
</Button>

{/* Embedded Camera Stream */}
{showCamera && (
  <div className="mt-3 border border-warning rounded-3 overflow-hidden">
    <img
      src="http://localhost:5050/camera"
      alt="Live Camera Stream"
      className="w-100"
      style={{
        height: "360px",
        objectFit: "cover",
        borderRadius: "10px",
      }}
    />
  </div>
)}

              </Card.Body>
            </Card>
          </Col>

        </Row>
      </Container>

      {/* Footer */}
      <footer className="bg-black text-center text-warning py-3 border-top border-warning mt-auto">
        © 2025 <span className="fw-bold text-light">EmotionSense</span> | Built by{" "}
        <span className="fw-bold text-warning">Rohan S. Bhat ⚡</span>
      </footer>
    </div>
  );
}
