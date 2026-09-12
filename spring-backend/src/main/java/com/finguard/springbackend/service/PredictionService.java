package com.finguard.springbackend.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.finguard.springbackend.dto.PredictionResponse;
import com.finguard.springbackend.dto.TransactionRequest;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class PredictionService {

    private final FastApiClient fastApiClient;
    private final ObjectMapper objectMapper;

    public PredictionService(
            FastApiClient fastApiClient,
            ObjectMapper objectMapper
    ) {
        this.fastApiClient = fastApiClient;
        this.objectMapper = objectMapper;
    }

    public PredictionResponse predict(
            TransactionRequest request,
            String jwtToken
    ) {
        Map<String, Object> transaction = objectMapper.convertValue(
                request,
                Map.class
        );

        String response = fastApiClient.predict(transaction, jwtToken);

        try {
            return objectMapper.readValue(
                    response,
                    PredictionResponse.class
            );
        } catch (Exception e) {
            throw new IllegalStateException(
                    "Failed to parse prediction response.",
                    e
            );
        }
    }
}