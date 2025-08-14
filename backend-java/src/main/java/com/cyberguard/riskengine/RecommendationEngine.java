package com.cyberguard.riskengine;

import java.util.ArrayList;
import java.util.List;

public class RecommendationEngine {
    public List<String> generateRecommendations(NetworkEntity entity, List<ThreatIndicator> threats) {
        List<String> recommendations = new ArrayList<>();
        
        // General recommendations
        recommendations.add("Ensure all security patches are applied");
        recommendations.add("Review firewall configurations");
        
        // Threat-specific recommendations
        for (ThreatIndicator threat : threats) {
            switch (threat.getType()) {
                case MALWARE:
                    recommendations.add("Run anti-malware scan on " + entity.getName());
                    break;
                case UNAUTHORIZED_ACCESS:
                    recommendations.add("Audit user accounts and permissions on " + entity.getName());
                    break;
                case DDOS:
                    recommendations.add("Implement DDOS protection for " + entity.getIp());
                    break;
                case DATA_LEAK:
                    recommendations.add("Review data access logs on " + entity.getName());
                    break;
                case CONFIGURATION_ERROR:
                    recommendations.add("Validate system configuration on " + entity.getName());
                    break;
            }
        }
        
        return recommendations;
    }
}