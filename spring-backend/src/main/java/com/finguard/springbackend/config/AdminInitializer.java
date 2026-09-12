package com.finguard.springbackend.config;

import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.repository.UserRepository;
import com.finguard.springbackend.security.PasswordService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class AdminInitializer implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(AdminInitializer.class);

    private final UserRepository userRepository;
    private final PasswordService passwordService;
    private final String adminUsername;
    private final String adminEmail;
    private final String adminPassword;

    public AdminInitializer(
            UserRepository userRepository,
            PasswordService passwordService,
            @Value("${ADMIN_USERNAME:#{null}}") String adminUsername,
            @Value("${ADMIN_EMAIL:#{null}}") String adminEmail,
            @Value("${ADMIN_PASSWORD:#{null}}") String adminPassword
    ) {
        this.userRepository = userRepository;
        this.passwordService = passwordService;
        this.adminUsername = adminUsername;
        this.adminEmail = adminEmail;
        this.adminPassword = adminPassword;
    }

    @Override
    public void run(String... args) {
        if (adminUsername == null || adminUsername.isBlank() ||
            adminEmail == null || adminEmail.isBlank() ||
            adminPassword == null || adminPassword.isBlank()) {
            logger.info("Admin bootstrap: ADMIN_USERNAME, ADMIN_EMAIL, or ADMIN_PASSWORD not configured.");
            return;
        }

        boolean exists = userRepository.existsByUsername(adminUsername) || userRepository.existsByEmail(adminEmail);

        if (!exists) {
            User admin = new User();
            admin.setUsername(adminUsername);
            admin.setEmail(adminEmail);
            admin.setHashedPassword(passwordService.hashPassword(adminPassword));
            admin.setRole("ADMIN");
            admin.setActive(true);

            userRepository.save(admin);
            logger.info("Admin bootstrap: Account '{}' created successfully with ROLE = ADMIN.", adminUsername);
        } else {
            logger.info("Admin bootstrap: Account '{}' already exists.", adminUsername);
        }
    }
}
