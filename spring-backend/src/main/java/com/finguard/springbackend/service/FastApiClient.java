package com.finguard.springbackend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class FastApiClient {

    private final RestClient restClient;

    public FastApiClient(
            @Value("${finguard.fastapi.base-url}") String fastApiBaseUrl
    ) {
        this.restClient = RestClient.builder()
                .baseUrl(fastApiBaseUrl)
                .build();
    }

    public String healthCheck() {
        return restClient.get()
                .uri("/health")
                .retrieve()
                .body(String.class);
    }

    public String predict(Map<String, Object> transaction, String jwtToken) {
        return restClient.post()
                .uri("/predict")
                .header("Authorization", "Bearer " + jwtToken)
                .contentType(MediaType.APPLICATION_JSON)
                .body(transaction)
                .retrieve()
                .body(String.class);
    }
}