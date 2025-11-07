package com.emotionsense;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class EmotionBackendApplication {
    public static void main(String[] args) {
        SpringApplication.run(EmotionBackendApplication.class, args);
        System.out.println("🚀 EmotionSense Backend Started Successfully!");
    }
}
