package com.cyberguard.riskengine;

import java.util.List;
import java.util.Map;

public class RiskAssessment {
    private String entityName;
    private double riskScore;
    private List<ThreatIndicator> threats;
    private List<String> recommendations;
    private NetworkMetrics metrics;
    
    public RiskAssessment(String entityName, double riskScore, 
                         List<ThreatIndicator> threats, 
                         List<String> recommendations,
                         NetworkMetrics metrics) {
        this.entityName = entityName;
        this.riskScore = riskScore;
        this.threats = threats;
        this.recommendations = recommendations;
        this.metrics = metrics;
    }
    
    public String toJson() {
        StringBuilder json = new StringBuilder("{");
        json.append("\"entity\":\"").append(entityName).append("\",");
        json.append("\"riskScore\":").append(String.format("%.2f", riskScore)).append(",");
        json.append("\"threats\":[");
        
        for (int i = 0; i < threats.size(); i++) {
            if (i > 0) json.append(",");
            json.append(threats.get(i).toJson());
        }
        
        json.append("],\"recommendations\":[");
        
        for (int i = 0; i < recommendations.size(); i++) {
            if (i > 0) json.append(",");
            json.append("\"").append(recommendations.get(i)).append("\"");
        }
        
        json.append("]}");
        return json.toString();
    }
    
    public static String toJson(Map<String, RiskAssessment> assessments) {
        StringBuilder json = new StringBuilder("{");
        boolean first = true;
        
        for (Map.Entry<String, RiskAssessment> entry : assessments.entrySet()) {
            if (!first) json.append(",");
            json.append("\"").append(entry.getKey()).append("\":").append(entry.getValue().toJson());
            first = false;
        }
        
        json.append("}");
        return json.toString();
    }
}