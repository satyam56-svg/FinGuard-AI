package com.finguard.springbackend.controller;

import com.finguard.springbackend.dto.AdminUserResponse;
import com.finguard.springbackend.dto.RoleUpdateRequest;
import com.finguard.springbackend.dto.UserStatusUpdateRequest;
import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.service.AdminService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/admin")
public class AdminController {

    private final AdminService adminService;

    public AdminController(AdminService adminService) {
        this.adminService = adminService;
    }

    @GetMapping("/dashboard")
    public Map<String, String> dashboard(Authentication authentication) {

        User currentAdmin = (User) authentication.getPrincipal();

        return Map.of(
                "message", "Admin dashboard access granted.",
                "username", currentAdmin.getUsername(),
                "role", currentAdmin.getRole()
        );
    }

    @GetMapping("/users")
    public List<AdminUserResponse> getAllUsers() {

        return adminService.getAllUsers()
                .stream()
                .map(user -> new AdminUserResponse(
                        user.getId(),
                        user.getUsername(),
                        user.getEmail(),
                        user.getRole(),
                        user.isActive()
                ))
                .toList();
    }

    @PatchMapping("/users/{user_id}/role")
    public AdminUserResponse updateRole(
            @PathVariable("user_id") Long userId,
            @Valid @RequestBody RoleUpdateRequest request,
            Authentication authentication
    ) {
        User currentAdmin = (User) authentication.getPrincipal();

        try {
            User updatedUser = adminService.updateUserRole(
                    userId,
                    request.role(),
                    currentAdmin.getId()
            );

            return new AdminUserResponse(
                    updatedUser.getId(),
                    updatedUser.getUsername(),
                    updatedUser.getEmail(),
                    updatedUser.getRole(),
                    updatedUser.isActive()
            );

        } catch (IllegalArgumentException exc) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    exc.getMessage()
            );
        }
    }

    @PatchMapping("/users/{user_id}/status")
    public AdminUserResponse updateStatus(
            @PathVariable("user_id") Long userId,
            @Valid @RequestBody UserStatusUpdateRequest request,
            Authentication authentication
    ) {
        User currentAdmin = (User) authentication.getPrincipal();

        try {
            User updatedUser = adminService.updateUserStatus(
                    userId,
                    request.is_active(),
                    currentAdmin.getId()
            );

            return new AdminUserResponse(
                    updatedUser.getId(),
                    updatedUser.getUsername(),
                    updatedUser.getEmail(),
                    updatedUser.getRole(),
                    updatedUser.isActive()
            );

        } catch (IllegalArgumentException exc) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    exc.getMessage()
            );
        }
    }
}