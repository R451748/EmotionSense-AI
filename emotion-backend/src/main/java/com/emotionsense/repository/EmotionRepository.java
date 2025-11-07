package com.emotionsense.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.emotionsense.model.EmotionRecord;

public interface EmotionRepository extends JpaRepository<EmotionRecord, Long> {}
