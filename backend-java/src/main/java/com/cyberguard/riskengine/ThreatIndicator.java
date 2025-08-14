package com.cyberguard.riskengine;

public class ThreatIndicator {
    public enum ThreatType {
        MALWARE, UNAUTHORIZED_ACCESS, DATA_LEAK, DDOS, CONFIGURATION_ERROR
    }
    
    private ThreatType type;
    private String description;
    private double severity;
    
    public ThreatIndicator(ThreatType type, String description, double severity) {
        this.type = type;
        this.description = description;
        this.severity = severity;
    }
    
    // Getters
    public ThreatType getType() { return type; }
    public String getDescription() { return description; }
    public double getSeverity() { return severity; }
    
    public String toJson() {
        return String.format(
            "{\"type\":\"%s\",\"description\":\"%s\",\"severity\":%.2f}",
            type, description, severity
        );
    }
}