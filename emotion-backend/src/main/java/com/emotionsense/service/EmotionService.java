package com.emotionsense.service;
import org.springframework.stereotype.Service;

import com.emotionsense.model.EmotionRecord;
import com.emotionsense.repository.EmotionRepository;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class EmotionService {

    private final EmotionRepository emotionRepository;

    public EmotionService(EmotionRepository emotionRepository) {
        this.emotionRepository = emotionRepository;
    }

    public EmotionRecord saveEmotion(EmotionRecord record) {
        record.setTimestamp(LocalDateTime.now());
        return emotionRepository.save(record);
    }

    public List<EmotionRecord> getAllEmotions() {
        return emotionRepository.findAll();
    }

    public EmotionRecord getEmotionById(Long id) {
        return emotionRepository.findById(id).orElse(null);
    }

    public void deleteEmotion(Long id) {
        emotionRepository.deleteById(id);
    }
}
