package com.finguard.springbackend.repository;

import com.finguard.springbackend.entity.PredictionAudit;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PredictionAuditRepository extends JpaRepository<PredictionAudit, Long> {

    List<PredictionAudit> findByUserIdOrderByCreatedAtDesc(Long userId);
}