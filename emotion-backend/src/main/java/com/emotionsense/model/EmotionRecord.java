package com.emotionsense.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "emotion_records")
public class EmotionRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String modality;     // facial, voice, text
    private String emotion;      // happy, sad, angry, etc.
    private double confidence;   // prediction accuracy
    private String sourceFile;   // file name or input reference
    private LocalDateTime timestamp;

    public EmotionRecord() {}

    public EmotionRecord(String modality, String emotion, double confidence, String sourceFile, LocalDateTime timestamp) {
        this.modality = modality;
        this.emotion = emotion;
        this.confidence = confidence;
        this.sourceFile = sourceFile;
        this.timestamp = timestamp;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getModality() { return modality; }
    public void setModality(String modality) { this.modality = modality; }

    public String getEmotion() { return emotion; }
    public void setEmotion(String emotion) { this.emotion = emotion; }

    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }

    public String getSourceFile() { return sourceFile; }
    public void setSourceFile(String sourceFile) { this.sourceFile = sourceFile; }

    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
}
