package com.cyberguard.riskengine;

public class NetworkEntity {
    private String name;
    private String ip;
    private String operatingSystem;
    
    public NetworkEntity(String name, String ip, String operatingSystem) {
        this.name = name;
        this.ip = ip;
        this.operatingSystem = operatingSystem;
    }
    
    // Getters
    public String getName() { return name; }
    public String getIp() { return ip; }
    public String getOperatingSystem() { return operatingSystem; }
    
    // Setters
    public void setName(String name) { this.name = name; }
    public void setIp(String ip) { this.ip = ip; }
    public void setOperatingSystem(String os) { this.operatingSystem = os; }
}