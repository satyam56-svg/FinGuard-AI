package com.finguard.springbackend.dto;

import java.util.List;

public record Explanation(
        List<ExplanationFactor> risk_factors,
        List<ExplanationFactor> protective_factors
) {
}