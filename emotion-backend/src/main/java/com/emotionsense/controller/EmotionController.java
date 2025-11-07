package com.emotionsense.controller;
import org.springframework.web.bind.annotation.*;

import com.emotionsense.model.EmotionRecord;
import com.emotionsense.service.EmotionService;

import java.util.List;

@RestController
@RequestMapping("/api/emotions")
@CrossOrigin(origins = "*")
public class EmotionController {

    private final EmotionService emotionService;

    public EmotionController(EmotionService emotionService) {
        this.emotionService = emotionService;
    }

    // POST: Save emotion record
    @PostMapping("/save")
    public EmotionRecord saveEmotion(@RequestBody EmotionRecord record) {
        return emotionService.saveEmotion(record);
    }

    // GET: All records
    @GetMapping("/all")
    public List<EmotionRecord> getAllEmotions() {
        return emotionService.getAllEmotions();
    }

    // GET: By ID
    @GetMapping("/{id}")
    public EmotionRecord getEmotionById(@PathVariable Long id) {
        return emotionService.getEmotionById(id);
    }

    // DELETE: Delete record
    @DeleteMapping("/{id}")
    public String deleteEmotion(@PathVariable Long id) {
        emotionService.deleteEmotion(id);
        return "Emotion record deleted successfully!";
    }
}
