package com.finguard.springbackend.service;

import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.repository.UserRepository;
import com.finguard.springbackend.security.PasswordService;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordService passwordService;

    public UserService(
            UserRepository userRepository,
            PasswordService passwordService
    ) {
        this.userRepository = userRepository;
        this.passwordService = passwordService;
    }

    public User createUser(
            String username,
            String email,
            String password
    ) {
        if (userRepository.existsByUsername(username)
                || userRepository.existsByEmail(email)) {
            throw new IllegalArgumentException(
                    "Username or email is already registered."
            );
        }

        User user = new User();
        user.setUsername(username);
        user.setEmail(email);
        user.setHashedPassword(passwordService.hashPassword(password));
        user.setRole("USER");
        user.setActive(true);

        return userRepository.save(user);
    }
}