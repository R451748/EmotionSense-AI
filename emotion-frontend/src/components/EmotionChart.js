import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function EmotionChart({ records }) {
  if (!records || records.length === 0) return null;

  const emotionCount = records.reduce((acc, r) => {
    acc[r.emotion] = (acc[r.emotion] || 0) + 1;
    return acc;
  }, {});

  const data = {
    labels: Object.keys(emotionCount),
    datasets: [
      {
        label: "Emotion Frequency",
        data: Object.values(emotionCount),
        backgroundColor: ["#00c6ff", "#007bff", "#6610f2", "#20c997", "#ffc107", "#dc3545"],
        borderRadius: 8,
      },
    ],
  };

  return (
    <div className="card mt-4 border-0 shadow-lg rounded-4">
      <div className="card-body">
        <h5 className="fw-bold text-primary mb-3">
          <i className="bi bi-graph-up"></i> Emotion Frequency
        </h5>
        <Bar data={data} />
      </div>
    </div>
  );
}
