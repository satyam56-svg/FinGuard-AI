package com.finguard.springbackend.dto;

public record AdminUserResponse(
        Long id,
        String username,
        String email,
        String role,
        boolean is_active
) {}