import React from "react";
import { Container } from "react-bootstrap";

export default function About() {
  return (
    <Container className="text-center py-5 text-light bg-dark min-vh-100">
      <h2 className="text-warning fw-bold mb-3">About EmotionSense</h2>
      <p className="lead">
        EmotionSense is a smart AI-powered tool that detects and analyzes emotions from text, 
        audio, and images using deep learning. Built with React, Flask, and TensorFlow, 
        it aims to bridge human emotion with intelligent systems.
      </p>
    </Container>
  );
}
