package com.finguard.springbackend.service;

import com.finguard.springbackend.dto.PredictionResponse;
import com.finguard.springbackend.entity.PredictionAudit;
import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.repository.PredictionAuditRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class PredictionAuditService {

    private final PredictionAuditRepository predictionAuditRepository;

    public PredictionAuditService(
            PredictionAuditRepository predictionAuditRepository
    ) {
        this.predictionAuditRepository = predictionAuditRepository;
    }

    public PredictionAudit createAudit(
            User user,
            PredictionResponse predictionResponse
    ) {
        PredictionAudit audit = new PredictionAudit();

        audit.setUser(user);
        audit.setPrediction(predictionResponse.prediction());
        audit.setFraudProbability(predictionResponse.fraud_probability());
        audit.setRiskScore(predictionResponse.risk_score());
        audit.setRiskLevel(predictionResponse.risk_level());
        audit.setRecommendation(predictionResponse.recommendation());
        audit.setCreatedAt(LocalDateTime.now());

        return predictionAuditRepository.save(audit);
    }
}