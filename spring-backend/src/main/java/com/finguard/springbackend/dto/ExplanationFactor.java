package com.finguard.springbackend.dto;

public record ExplanationFactor(
        String feature,
        double value,
        double impact,
        String direction
) {
}