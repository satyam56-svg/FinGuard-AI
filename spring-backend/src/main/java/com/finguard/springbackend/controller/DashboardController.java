package com.finguard.springbackend.controller;

import com.finguard.springbackend.entity.PredictionAudit;
import com.finguard.springbackend.service.DashboardService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/analyst")
public class DashboardController {

    private final DashboardService dashboardService;

    public DashboardController(DashboardService dashboardService) {
        this.dashboardService = dashboardService;
    }

    @GetMapping("/dashboard/stats")
    public Map<String, Object> getDashboardStats() {
        return dashboardService.getDashboardStats();
    }

    @GetMapping("/dashboard/risk-distribution")
    public Map<String, Integer> getRiskDistribution() {
        return dashboardService.getRiskDistribution();
    }

    @GetMapping("/dashboard/recent-predictions")
    public List<Map<String, Object>> getRecentPredictions() {

        return dashboardService.getRecentPredictions()
                .stream()
                .map(audit -> {
                    Map<String, Object> result = new HashMap<>();

                    result.put("id", audit.getId());
                    result.put("prediction", audit.getPrediction());
                    result.put("fraud_probability", audit.getFraudProbability());
                    result.put("risk_score", audit.getRiskScore());
                    result.put("risk_level", audit.getRiskLevel());
                    result.put("recommendation", audit.getRecommendation());
                    result.put("created_at", audit.getCreatedAt());

                    return result;
                })
                .toList();
    }
}