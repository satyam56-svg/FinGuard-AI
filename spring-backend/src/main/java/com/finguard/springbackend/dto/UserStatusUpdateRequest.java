package com.finguard.springbackend.dto;

import jakarta.validation.constraints.NotNull;

public record UserStatusUpdateRequest(
        @NotNull Boolean is_active
) {}