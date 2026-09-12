package com.finguard.springbackend.service;

import com.finguard.springbackend.entity.User;
import com.finguard.springbackend.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AdminService {

    private final UserRepository userRepository;

    public AdminService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll()
                .stream()
                .sorted((a, b) -> a.getId().compareTo(b.getId()))
                .toList();
    }

    public User updateUserRole(
            Long userId,
            String newRole,
            Long currentAdminId
    ) {
        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "User not found."
                        )
                );

        if (!newRole.equals("USER")
                && !newRole.equals("ANALYST")
                && !newRole.equals("ADMIN")) {
            throw new IllegalArgumentException(
                    "Invalid role. Allowed roles: USER, ANALYST, ADMIN."
            );
        }

        if (user.getId().equals(currentAdminId)) {
            throw new IllegalArgumentException(
                    "Admin cannot change their own role."
            );
        }

        user.setRole(newRole);

        return userRepository.save(user);
    }

    public User updateUserStatus(
            Long userId,
            boolean isActive,
            Long currentAdminId
    ) {
        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "User not found."
                        )
                );

        if (user.getId().equals(currentAdminId) && !isActive) {
            throw new IllegalArgumentException(
                    "Admin cannot deactivate their own account."
            );
        }

        user.setActive(isActive);

        return userRepository.save(user);
    }
}