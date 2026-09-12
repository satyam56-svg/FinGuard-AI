package com.finguard.springbackend.service;

import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.repository.UserRepository;
import com.finguard.springbackend.security.JwtService;
import com.finguard.springbackend.security.PasswordService;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordService passwordService;
    private final JwtService jwtService;

    public AuthService(
            UserRepository userRepository,
            PasswordService passwordService,
            JwtService jwtService
    ) {
        this.userRepository = userRepository;
        this.passwordService = passwordService;
        this.jwtService = jwtService;
    }

    public String login(String username, String password) {

        User user = userRepository.findByUsername(username)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Invalid username or password."
                        )
                );

        if (!user.isActive()) {
            throw new IllegalArgumentException(
                    "User account is inactive."
            );
        }

        if (!passwordService.verifyPassword(
                password,
                user.getHashedPassword()
        )) {
            throw new IllegalArgumentException(
                    "Invalid username or password."
            );
        }

        return jwtService.generateToken(user);
    }
}