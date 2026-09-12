package com.finguard.springbackend.dto;

public record AIReport(
        String summary,
        String risk_reason,
        String recommended_action
) {
}