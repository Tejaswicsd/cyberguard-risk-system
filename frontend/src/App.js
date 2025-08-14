import React, { useState, useEffect } from 'react';
import { AlertTriangle, Shield, TrendingUp, Users, Settings, Eye } from 'lucide-react';

const CyberRiskDashboard = () => {
  const [entities, setEntities] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [riskAnalysis, setRiskAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock data for demonstration
  const mockEntities = [
    { id: 1, name: 'Database Server', ip: '192.168.1.100', riskScore: 42, status: 'medium' },
    { id: 2, name: 'Web Server', ip: '192.168.1.200', riskScore: 75, status: 'high' },
    { id: 3, name: 'Email Server', ip: '192.168.1.150', riskScore: 28, status: 'low' },
    { id: 4, name: 'File Server', ip: '192.168.1.120', riskScore: 58, status: 'medium' },
    { id: 5, name: 'Domain Controller', ip: '192.168.1.10', riskScore: 85, status: 'critical' }
  ];

  const mockRiskFactors = [
    { factor: 'Open Ports', impact: 85, recommendation: 'Close unnecessary ports 22, 445' },
    { factor: 'Outdated Software', impact: 70, recommendation: 'Update system patches' },
    { factor: 'Weak Passwords', impact: 60, recommendation: 'Enforce strong password policy' },
    { factor: 'Failed Login Attempts', impact: 45, recommendation: 'Review authentication logs' }
  ];

  useEffect(() => {
    setEntities(mockEntities);
  }, [mockEntities]);

  const calculateRiskScore = (entity) => {
    setLoading(true);
    // Simulate ML model prediction
    setTimeout(() => {
      const analysis = {
        currentScore: entity.riskScore,
        predictedScore: Math.min(100, entity.riskScore + Math.floor(Math.random() * 20) - 10),
        factors: mockRiskFactors,
        trend: Math.random() > 0.5 ? 'increasing' : 'decreasing',
        recommendations: [
          'Update firewall rules to restrict access',
          'Enable multi-factor authentication',
          'Schedule regular security scans',
          'Monitor network traffic patterns'
        ]
      };
      setRiskAnalysis(analysis);
      setLoading(false);
    }, 1500);
  };

  const getRiskColor = (score) => {
    if (score >= 80) return 'text-red-600 bg-red-100';
    if (score >= 60) return 'text-orange-600 bg-orange-100';
    if (score >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getRiskLevel = (score) => {
    if (score >= 80) return 'Critical';
    if (score >= 60) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-3">
            <Shield className="h-8 w-8 text-blue-400" />
            <h1 className="text-3xl font-bold text-white">CyberGuard Risk Analytics</h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-gray-300">Last Update</p>
              <p className="text-white font-medium">{new Date().toLocaleTimeString()}</p>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Total Entities</p>
                <p className="text-2xl font-bold text-white">{entities.length}</p>
              </div>
              <Users className="h-8 w-8 text-blue-400" />
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Average Risk</p>
                <p className="text-2xl font-bold text-white">
                  {Math.round(entities.reduce((sum, e) => sum + e.riskScore, 0) / entities.length || 0)}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-orange-400" />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Critical Alerts</p>
                <p className="text-2xl font-bold text-red-400">
                  {entities.filter(e => e.riskScore >= 80).length}
                </p>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-400" />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Monitored</p>
                <p className="text-2xl font-bold text-green-400">24/7</p>
              </div>
              <Eye className="h-8 w-8 text-green-400" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Entity List */}
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <h2 className="text-xl font-semibold text-white mb-4">Network Entities</h2>
            <div className="space-y-3">
              {entities.map((entity) => (
                <div
                  key={entity.id}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedEntity?.id === entity.id
                      ? 'border-blue-400 bg-blue-900/30'
                      : 'border-white/20 bg-white/5 hover:bg-white/10'
                  }`}
                  onClick={() => setSelectedEntity(entity)}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-white">{entity.name}</h3>
                      <p className="text-sm text-gray-300">{entity.ip}</p>
                    </div>
                    <div className="text-right">
                      <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(entity.riskScore)}`}>
                        {entity.riskScore}/100
                      </div>
                      <p className="text-xs text-gray-400 mt-1">{getRiskLevel(entity.riskScore)}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Risk Analysis Panel */}
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-white">Risk Analysis</h2>
              {selectedEntity && (
                <button
                  onClick={() => calculateRiskScore(selectedEntity)}
                  disabled={loading}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  <Settings className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                  <span>{loading ? 'Analyzing...' : 'Analyze Risk'}</span>
                </button>
              )}
            </div>

            {!selectedEntity ? (
              <div className="text-center py-12">
                <Shield className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-300">Select an entity to view risk analysis</p>
              </div>
            ) : loading ? (
              <div className="text-center py-12">
                <div className="animate-spin h-16 w-16 border-4 border-blue-400 border-t-transparent rounded-full mx-auto mb-4"></div>
                <p className="text-gray-300">Running ML risk assessment...</p>
              </div>
            ) : riskAnalysis ? (
              <div className="space-y-6">
                <div>
                  <h3 className="font-medium text-white mb-2">Risk Score Prediction</h3>
                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <p className="text-sm text-gray-300">Current</p>
                      <p className={`text-2xl font-bold ${getRiskColor(riskAnalysis.currentScore).split(' ')[0]}`}>
                        {riskAnalysis.currentScore}
                      </p>
                    </div>
                    <div className="flex-1 h-2 bg-gray-700 rounded">
                      <div 
                        className="h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded"
                        style={{ width: `${riskAnalysis.currentScore}%` }}
                      ></div>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-300">Predicted</p>
                      <p className={`text-2xl font-bold ${getRiskColor(riskAnalysis.predictedScore).split(' ')[0]}`}>
                        {riskAnalysis.predictedScore}
                      </p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="font-medium text-white mb-3">Top Risk Factors</h3>
                  <div className="space-y-3">
                    {riskAnalysis.factors.map((factor, index) => (
                      <div key={index} className="bg-white/5 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-white text-sm">{factor.factor}</span>
                          <span className="text-orange-400 font-medium">{factor.impact}%</span>
                        </div>
                        <p className="text-xs text-gray-300">{factor.recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-medium text-white mb-3">Recommendations</h3>
                  <div className="space-y-2">
                    {riskAnalysis.recommendations.map((rec, index) => (
                      <div key={index} className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-blue-400 rounded-full mt-2"></div>
                        <p className="text-sm text-gray-300">{rec}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <AlertTriangle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-300">Click "Analyze Risk" to generate assessment</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CyberRiskDashboard;