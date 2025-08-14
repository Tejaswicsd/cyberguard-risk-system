package com.cyberguard.riskengine;

public class NetworkMetrics {
    private double cpuUsage;
    private double memoryUsage;
    private double networkActivity;
    
    public NetworkMetrics(double cpuUsage, double memoryUsage, double networkActivity) {
        this.cpuUsage = cpuUsage;
        this.memoryUsage = memoryUsage;
        this.networkActivity = networkActivity;
    }
    
    // Getters
    public double getCpuUsage() { return cpuUsage; }
    public double getMemoryUsage() { return memoryUsage; }
    public double getNetworkActivity() { return networkActivity; }
}