import React from "react";

export default function EmotionTable({ records }) {
  if (!records || records.length === 0)
    return <p className="text-center text-muted mt-3">No emotion records yet 😴</p>;

  return (
    <div className="card mt-4 border-0 shadow-lg rounded-4">
      <div className="card-body">
        <h5 className="fw-bold text-primary mb-3">
          <i className="bi bi-bar-chart"></i> Recent Emotion Records
        </h5>
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th>ID</th>
                <th>Modality</th>
                <th>Emotion</th>
                <th>Confidence</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id}>
                  <td>{r.id}</td>
                  <td>{r.modality}</td>
                  <td>
                    <span className="badge bg-info text-dark">{r.emotion}</span>
                  </td>
                  <td>{r.confidence?.toFixed(2)}</td>
                  <td>{r.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
