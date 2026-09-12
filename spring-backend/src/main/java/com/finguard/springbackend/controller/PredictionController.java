package com.finguard.springbackend.controller;

import com.finguard.springbackend.dto.PredictionResponse;
import com.finguard.springbackend.dto.TransactionRequest;
import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.service.PredictionAuditService;
import com.finguard.springbackend.service.PredictionService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
public class PredictionController {

    private final PredictionService predictionService;
    private final PredictionAuditService predictionAuditService;

    public PredictionController(
            PredictionService predictionService,
            PredictionAuditService predictionAuditService
    ) {
        this.predictionService = predictionService;
        this.predictionAuditService = predictionAuditService;
    }

    @PostMapping("/predict")
    public ResponseEntity<PredictionResponse> predict(
            @Valid @RequestBody TransactionRequest request,
            HttpServletRequest httpRequest,
            Authentication authentication
    ) {
        String authHeader = httpRequest.getHeader("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return ResponseEntity.status(401).build();
        }

        String jwtToken = authHeader.substring(7);

        PredictionResponse response =
                predictionService.predict(request, jwtToken);

        User currentUser = (User) authentication.getPrincipal();

        predictionAuditService.createAudit(
                currentUser,
                response
        );

        return ResponseEntity.ok(response);
    }
}