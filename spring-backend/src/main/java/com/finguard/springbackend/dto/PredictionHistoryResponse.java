package com.finguard.springbackend.dto;

import java.time.LocalDateTime;

public record PredictionHistoryResponse(
        Long id,
        int prediction,
        double fraud_probability,
        double risk_score,
        String risk_level,
        String recommendation,
        LocalDateTime created_at
) {
}