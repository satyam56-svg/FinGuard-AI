package com.finguard.springbackend.security;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class PasswordService {

    private final BCryptPasswordEncoder passwordEncoder;

    public PasswordService() {
        this.passwordEncoder = new BCryptPasswordEncoder();
    }

    public String hashPassword(String password) {
        if (password.getBytes(java.nio.charset.StandardCharsets.UTF_8).length > 72) {
            throw new IllegalArgumentException(
                    "Password cannot be longer than 72 bytes."
            );
        }

        return passwordEncoder.encode(password);
    }

    public boolean verifyPassword(String plainPassword, String hashedPassword) {
        if (plainPassword.getBytes(java.nio.charset.StandardCharsets.UTF_8).length > 72) {
            return false;
        }

        return passwordEncoder.matches(plainPassword, hashedPassword);
    }
}