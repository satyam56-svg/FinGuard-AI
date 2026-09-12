package com.finguard.springbackend.service;

import com.finguard.springbackend.entity.PredictionAudit;
import com.finguard.springbackend.repository.PredictionAuditRepository;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DashboardService {

    private final PredictionAuditRepository predictionAuditRepository;

    public DashboardService(PredictionAuditRepository predictionAuditRepository) {
        this.predictionAuditRepository = predictionAuditRepository;
    }

    public Map<String, Object> getDashboardStats() {

        List<PredictionAudit> audits = predictionAuditRepository.findAll();

        long totalPredictions = audits.size();

        long fraudPredictions = audits.stream()
                .filter(audit -> audit.getPrediction() == 1)
                .count();

        long nonFraudPredictions =
                totalPredictions - fraudPredictions;

        double fraudRate =
                totalPredictions > 0
                        ? ((double) fraudPredictions / totalPredictions) * 100
                        : 0.0;

        double averageRiskScore =
                audits.stream()
                        .mapToDouble(PredictionAudit::getRiskScore)
                        .average()
                        .orElse(0.0);

        Map<String, Object> result = new HashMap<>();

        result.put("total_predictions", totalPredictions);
        result.put("fraud_predictions", fraudPredictions);
        result.put("non_fraud_predictions", nonFraudPredictions);
        result.put("fraud_rate", Math.round(fraudRate * 100.0) / 100.0);
        result.put(
                "average_risk_score",
                Math.round(averageRiskScore * 100.0) / 100.0
        );

        return result;
    }

    public Map<String, Integer> getRiskDistribution() {

        List<PredictionAudit> audits =
                predictionAuditRepository.findAll();

        Map<String, Integer> distribution = new HashMap<>();

        distribution.put("low", 0);
        distribution.put("medium", 0);
        distribution.put("high", 0);
        distribution.put("critical", 0);

        for (PredictionAudit audit : audits) {

            String key =
                    audit.getRiskLevel().toLowerCase();

            if (distribution.containsKey(key)) {
                distribution.put(
                        key,
                        distribution.get(key) + 1
                );
            }
        }

        return distribution;
    }

    public List<PredictionAudit> getRecentPredictions() {

        List<PredictionAudit> audits =
                predictionAuditRepository.findAll();

        return audits.stream()
                .sorted(
                        (a, b) -> b.getCreatedAt()
                                .compareTo(a.getCreatedAt())
                )
                .limit(10)
                .toList();
    }
}