package com.finguard.springbackend.controller;

import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.service.AuthService;
import com.finguard.springbackend.service.UserService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;
    private final UserService userService;

    public AuthController(
            AuthService authService,
            UserService userService
    ) {
        this.authService = authService;
        this.userService = userService;
    }

    @PostMapping("/register")
    public ResponseEntity<UserResponse> register(
            @Valid @RequestBody RegisterRequest request
    ) {
        try {
            User createdUser = userService.createUser(
                    request.username(),
                    request.email(),
                    request.password()
            );

            UserResponse response = new UserResponse(
                    createdUser.getId(),
                    createdUser.getUsername(),
                    createdUser.getEmail(),
                    createdUser.getRole(),
                    createdUser.isActive()
            );

            return ResponseEntity
                    .status(HttpStatus.CREATED)
                    .body(response);

        } catch (IllegalArgumentException exc) {
            return ResponseEntity
                    .status(HttpStatus.CONFLICT)
                    .build();
        }
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(
            @Valid @RequestBody LoginRequest request
    ) {
        try {
            String token = authService.login(
                    request.username(),
                    request.password()
            );

            return ResponseEntity.ok(
                    new LoginResponse(token)
            );

        } catch (IllegalArgumentException exc) {
            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .build();
        }
    }

    public record RegisterRequest(
            @NotBlank
            @Size(min = 3, max = 50)
            String username,

            @NotBlank
            @Email
            @Size(min = 5, max = 255)
            String email,

            @NotBlank
            @Size(min = 8, max = 72)
            String password
    ) {}

    public record LoginRequest(
            @NotBlank String username,
            @NotBlank String password
    ) {}

    public record LoginResponse(String access_token) {}

    public record UserResponse(
            Long id,
            String username,
            String email,
            String role,
            boolean is_active
    ) {}
}