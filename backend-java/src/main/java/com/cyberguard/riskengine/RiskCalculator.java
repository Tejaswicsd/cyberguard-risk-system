package com.cyberguard.riskengine;

import java.util.List;

public class RiskCalculator {
    public double calculateRiskScore(NetworkEntity entity, NetworkMetrics metrics, List<ThreatIndicator> threats) {
        double baseScore = 0.3;
        
        // Add OS risk factor
        if (entity.getOperatingSystem().contains("Windows")) {
            baseScore += 0.2;
        } else if (entity.getOperatingSystem().contains("Ubuntu")) {
            baseScore += 0.1;
        }
        
        // Add metrics factors
        baseScore += metrics.getCpuUsage() * 0.002;
        baseScore += metrics.getMemoryUsage() * 0.002;
        baseScore += metrics.getNetworkActivity() * 0.001;
        
        // Add threat factors
        for (ThreatIndicator threat : threats) {
            baseScore += threat.getSeverity() * 0.2;
        }
        
        // Cap at 1.0 (100%)
        return Math.min(1.0, baseScore);
    }
}