package com.finguard.springbackend.controller;

import com.finguard.springbackend.dto.PredictionHistoryResponse;
import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.service.PredictionHistoryService;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/predictions")
public class PredictionHistoryController {

    private final PredictionHistoryService predictionHistoryService;

    public PredictionHistoryController(
            PredictionHistoryService predictionHistoryService
    ) {
        this.predictionHistoryService = predictionHistoryService;
    }

    @GetMapping("/history")
    public List<PredictionHistoryResponse> getHistory(
            Authentication authentication
    ) {
        User currentUser = (User) authentication.getPrincipal();

        return predictionHistoryService.getHistory(
                currentUser.getId()
        );
    }
}