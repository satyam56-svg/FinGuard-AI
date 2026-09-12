package com.finguard.springbackend.dto;

public record PredictionResponse(
        int prediction,
        double fraud_probability,
        double risk_score,
        String risk_level,
        String recommendation,
        Explanation explanation,
        AIReport ai_report
) {
}