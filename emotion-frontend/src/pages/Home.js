import React from "react";
import { Link } from "react-router-dom";
import { Container, Button } from "react-bootstrap";

export default function Home() {
  return (
    <div className="bg-dark text-light min-vh-100 d-flex align-items-center">
      <Container className="text-center">
        <h1 className="display-4 fw-bold text-warning">Welcome to EmotionSense</h1>
        <p className="lead mt-3">Analyze emotions from text, audio, and images with AI precision.</p>
        <Link to="/dashboard">
          <Button variant="warning" size="lg" className="mt-4 shadow">Get Started</Button>
        </Link>
      </Container>
    </div>
  );
}
