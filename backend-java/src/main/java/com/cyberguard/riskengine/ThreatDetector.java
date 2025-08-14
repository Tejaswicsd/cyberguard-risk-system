package com.cyberguard.riskengine;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ThreatDetector {
    public List<ThreatIndicator> detectThreats(NetworkEntity entity, NetworkMetrics metrics) {
        List<ThreatIndicator> threats = new ArrayList<>();
        Random random = new Random();
        
        // Simulate threat detection
        if (metrics.getCpuUsage() > 90) {
            threats.add(new ThreatIndicator(
                ThreatIndicator.ThreatType.DDOS,
                "High CPU usage indicating possible DDOS attack",
                0.8 + random.nextDouble() * 0.2
            ));
        }
        
        if (metrics.getMemoryUsage() > 85) {
            threats.add(new ThreatIndicator(
                ThreatIndicator.ThreatType.MALWARE,
                "High memory usage could indicate malware activity",
                0.7 + random.nextDouble() * 0.3
            ));
        }
        
        if (entity.getOperatingSystem().contains("Windows") && metrics.getNetworkActivity() > 80) {
            threats.add(new ThreatIndicator(
                ThreatIndicator.ThreatType.UNAUTHORIZED_ACCESS,
                "Unusual network activity on Windows system",
                0.6 + random.nextDouble() * 0.4
            ));
        }
        
        return threats;
    }
}