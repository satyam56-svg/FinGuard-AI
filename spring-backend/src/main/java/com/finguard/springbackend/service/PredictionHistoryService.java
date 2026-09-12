package com.finguard.springbackend.service;

import com.finguard.springbackend.dto.PredictionHistoryResponse;
import com.finguard.springbackend.entity.PredictionAudit;
import com.finguard.springbackend.repository.PredictionAuditRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PredictionHistoryService {

    private final PredictionAuditRepository predictionAuditRepository;

    public PredictionHistoryService(
            PredictionAuditRepository predictionAuditRepository
    ) {
        this.predictionAuditRepository = predictionAuditRepository;
    }

    public List<PredictionHistoryResponse> getHistory(Long userId) {

        List<PredictionAudit> audits =
                predictionAuditRepository
                        .findByUserIdOrderByCreatedAtDesc(userId);

        return audits.stream()
                .map(audit -> new PredictionHistoryResponse(
                        audit.getId(),
                        audit.getPrediction(),
                        audit.getFraudProbability(),
                        audit.getRiskScore(),
                        audit.getRiskLevel(),
                        audit.getRecommendation(),
                        audit.getCreatedAt()
                ))
                .toList();
    }
}