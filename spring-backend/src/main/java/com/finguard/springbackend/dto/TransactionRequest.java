package com.finguard.springbackend.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public record TransactionRequest(

        @NotNull
        Integer step,

        @NotNull
        String type,

        @NotNull
        @Min(0)
        Double amount,

        @NotNull
        @Min(0)
        Double oldbalanceOrg,

        @NotNull
        @Min(0)
        Double newbalanceOrig,

        @NotNull
        @Min(0)
        Double oldbalanceDest,

        @NotNull
        @Min(0)
        Double newbalanceDest,

        @NotNull
        @Min(0)
        @Max(1)
        Integer isFlaggedFraud,

        @NotNull
        Double origin_balance_error,

        @NotNull
        Double destination_balance_error,

        @NotNull
        Double origin_balance_change,

        @NotNull
        Double destination_balance_change
) {
}