import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import json
from datetime import datetime, timedelta
import random

class CyberRiskPredictor:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_training_data(self, n_samples=1000):
        """Generate synthetic cybersecurity data for training"""
        data = []
        
        for _ in range(n_samples):
            # Simulate network entity features
            record = {
                'open_ports': random.randint(0, 50),
                'failed_logins': random.randint(0, 100),
                'network_traffic_mb': random.uniform(0, 10000),
                'cpu_usage': random.uniform(0, 100),
                'memory_usage': random.uniform(0, 100),
                'disk_usage': random.uniform(0, 100),
                'patch_level': random.uniform(0, 1),  # 0 = outdated, 1 = up to date
                'firewall_rules': random.randint(0, 200),
                'antivirus_status': random.choice([0, 1]),  # 0 = disabled, 1 = enabled
                'encryption_level': random.uniform(0, 1),
                'user_privilege_level': random.randint(1, 5),  # 1 = admin, 5 = guest
                'connection_attempts': random.randint(0, 1000),
                'data_transfer_anomaly': random.uniform(0, 1),
                'login_time_anomaly': random.uniform(0, 1),
                'geographic_anomaly': random.uniform(0, 1)
            }
            
            # Calculate risk score based on features (for supervised learning)
            risk_factors = [
                record['open_ports'] / 50 * 0.15,
                record['failed_logins'] / 100 * 0.20,
                (100 - record['patch_level'] * 100) / 100 * 0.25,
                (1 - record['antivirus_status']) * 0.15,
                (1 - record['encryption_level']) * 0.10,
                (record['user_privilege_level'] - 1) / 4 * 0.05,
                record['data_transfer_anomaly'] * 0.05,
                record['login_time_anomaly'] * 0.03,
                record['geographic_anomaly'] * 0.02
            ]
            
            record['risk_score'] = min(100, sum(risk_factors) * 100)
            record['risk_category'] = self._categorize_risk(record['risk_score'])
            
            data.append(record)
        
        return pd.DataFrame(data)
    
    def _categorize_risk(self, score):
        """Categorize risk score into levels"""
        if score >= 80:
            return 3  # Critical
        elif score >= 60:
            return 2  # High
        elif score >= 40:
            return 1  # Medium
        else:
            return 0  # Low
    
    def train_models(self):
        """Train both Isolation Forest and Random Forest models"""
        print("Generating training data...")
        df = self.generate_training_data(1000)
        
        # Prepare features for training
        feature_columns = [
            'open_ports', 'failed_logins', 'network_traffic_mb', 'cpu_usage',
            'memory_usage', 'disk_usage', 'patch_level', 'firewall_rules',
            'antivirus_status', 'encryption_level', 'user_privilege_level',
            'connection_attempts', 'data_transfer_anomaly', 'login_time_anomaly',
            'geographic_anomaly'
        ]
        
        X = df[feature_columns]
        y = df['risk_category']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data for supervised learning
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train Isolation Forest (unsupervised anomaly detection)
        print("Training Isolation Forest...")
        self.isolation_forest.fit(X_scaled)
        
        # Train Random Forest (supervised classification)
        print("Training Random Forest...")
        self.random_forest.fit(X_train, y_train)
        
        # Evaluate models
        y_pred = self.random_forest.predict(X_test)
        print("\nRandom Forest Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Test anomaly detection
        anomaly_scores = self.isolation_forest.decision_function(X_test)
        anomalies = self.isolation_forest.predict(X_test)
        print(f"\nDetected {sum(anomalies == -1)} anomalies out of {len(X_test)} samples")
        
        self.is_trained = True
        print("Models trained successfully!")
        
    def predict_risk(self, entity_data):
        """Predict risk score for a single entity"""
        if not self.is_trained:
            print("Models not trained. Training now...")
            self.train_models()
        
        # Convert entity data to feature vector
        features = [
            entity_data.get('open_ports', 0),
            entity_data.get('failed_logins', 0),
            entity_data.get('network_traffic_mb', 0),
            entity_data.get('cpu_usage', 0),
            entity_data.get('memory_usage', 0),
            entity_data.get('disk_usage', 0),
            entity_data.get('patch_level', 1),
            entity_data.get('firewall_rules', 0),
            entity_data.get('antivirus_status', 1),
            entity_data.get('encryption_level', 1),
            entity_data.get('user_privilege_level', 3),
            entity_data.get('connection_attempts', 0),
            entity_data.get('data_transfer_anomaly', 0),
            entity_data.get('login_time_anomaly', 0),
            entity_data.get('geographic_anomaly', 0)
        ]
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Get predictions
        risk_category = self.random_forest.predict(features_scaled)[0]
        risk_probability = self.random_forest.predict_proba(features_scaled)[0]
        anomaly_score = self.isolation_forest.decision_function(features_scaled)[0]
        is_anomaly = self.isolation_forest.predict(features_scaled)[0] == -1
        
        # Calculate dynamic risk score
        base_risk = risk_probability[risk_category] * 100
        anomaly_adjustment = abs(anomaly_score) * 20 if is_anomaly else 0
        final_risk_score = min(100, base_risk + anomaly_adjustment)
        
        return {
            'risk_score': round(final_risk_score, 2),
            'risk_category': ['Low', 'Medium', 'High', 'Critical'][risk_category],
            'is_anomaly': bool(is_anomaly),
            'anomaly_score': round(anomaly_score, 4),
            'confidence': round(max(risk_probability) * 100, 2),
            'risk_factors': self._identify_risk_factors(entity_data, features)
        }
    
    def _identify_risk_factors(self, entity_data, features):
        """Identify the main risk factors contributing to the score"""
        risk_factors = []
        
        if entity_data.get('open_ports', 0) > 20:
            risk_factors.append({
                'factor': 'High number of open ports',
                'impact': min(100, entity_data.get('open_ports', 0) / 50 * 100),
                'recommendation': 'Close unnecessary ports and implement port scanning protection'
            })
        
        if entity_data.get('failed_logins', 0) > 50:
            risk_factors.append({
                'factor': 'Excessive failed login attempts',
                'impact': min(100, entity_data.get('failed_logins', 0) / 100 * 100),
                'recommendation': 'Implement account lockout policies and monitor for brute force attacks'
            })
        
        if entity_data.get('patch_level', 1) < 0.8:
            risk_factors.append({
                'factor': 'Outdated software/patches',
                'impact': (1 - entity_data.get('patch_level', 1)) * 100,
                'recommendation': 'Update system patches and implement automated patching'
            })
        
        if entity_data.get('antivirus_status', 1) == 0:
            risk_factors.append({
                'factor': 'Antivirus disabled',
                'impact': 80,
                'recommendation': 'Enable and update antivirus protection'
            })
        
        if entity_data.get('encryption_level', 1) < 0.7:
            risk_factors.append({
                'factor': 'Weak encryption',
                'impact': (1 - entity_data.get('encryption_level', 1)) * 80,
                'recommendation': 'Implement stronger encryption protocols'
            })
        
        return risk_factors
    
    def generate_recommendations(self, risk_assessment):
        """Generate actionable security recommendations"""
        recommendations = []
        
        if risk_assessment['risk_score'] > 80:
            recommendations.extend([
                'Immediate security audit required',
                'Isolate system until vulnerabilities are patched',
                'Enable advanced threat detection',
                'Implement emergency response procedures'
            ])
        elif risk_assessment['risk_score'] > 60:
            recommendations.extend([
                'Schedule security assessment within 24 hours',
                'Review and update security policies',
                'Enable additional monitoring',
                'Conduct penetration testing'
            ])
        elif risk_assessment['risk_score'] > 40:
            recommendations.extend([
                'Regular security monitoring recommended',
                'Update security configurations',
                'Review access controls',
                'Schedule routine maintenance'
            ])
        else:
            recommendations.extend([
                'Maintain current security posture',
                'Continue regular updates',
                'Monitor for changes',
                'Document security baseline'
            ])
        
        if risk_assessment['is_anomaly']:
            recommendations.append('Investigate anomalous behavior patterns')
        
        return recommendations
    
    def save_models(self, path='cyber_risk_models'):
        """Save trained models to disk"""
        if self.is_trained:
            joblib.dump(self.isolation_forest, f'{path}_isolation_forest.pkl')
            joblib.dump(self.random_forest, f'{path}_random_forest.pkl')
            joblib.dump(self.scaler, f'{path}_scaler.pkl')
            print(f"Models saved to {path}")
        else:
            print("No trained models to save")
    
    def load_models(self, path='cyber_risk_models'):
        """Load trained models from disk"""
        try:
            self.isolation_forest = joblib.load(f'{path}_isolation_forest.pkl')
            self.random_forest = joblib.load(f'{path}_random_forest.pkl')
            self.scaler = joblib.load(f'{path}_scaler.pkl')
            self.is_trained = True
            print(f"Models loaded from {path}")
        except FileNotFoundError:
            print("Model files not found. Training new models...")
            self.train_models()

# Example usage and API endpoint simulation
def main():
    # Initialize predictor
    predictor = CyberRiskPredictor()
    
    # Train models
    predictor.train_models()
    
    # Example entity data
    sample_entities = [
        {
            'name': 'Web Server',
            'ip': '192.168.1.200',
            'open_ports': 35,
            'failed_logins': 75,
            'network_traffic_mb': 5000,
            'cpu_usage': 85,
            'memory_usage': 70,
            'disk_usage': 60,
            'patch_level': 0.6,
            'firewall_rules': 50,
            'antivirus_status': 1,
            'encryption_level': 0.8,
            'user_privilege_level': 2,
            'connection_attempts': 500,
            'data_transfer_anomaly': 0.7,
            'login_time_anomaly': 0.3,
            'geographic_anomaly': 0.2
        },
        {
            'name': 'Database Server',
            'ip': '192.168.1.100',
            'open_ports': 15,
            'failed_logins': 25,
            'network_traffic_mb': 2000,
            'cpu_usage': 45,
            'memory_usage': 55,
            'disk_usage': 40,
            'patch_level': 0.9,
            'firewall_rules': 120,
            'antivirus_status': 1,
            'encryption_level': 0.95,
            'user_privilege_level': 4,
            'connection_attempts': 100,
            'data_transfer_anomaly': 0.1,
            'login_time_anomaly': 0.1,
            'geographic_anomaly': 0.05
        }
    ]
    
    # Predict risk for sample entities
    for entity in sample_entities:
        print(f"\n=== Risk Assessment for {entity['name']} ===")
        risk_assessment = predictor.predict_risk(entity)
        recommendations = predictor.generate_recommendations(risk_assessment)
        
        print(f"Risk Score: {risk_assessment['risk_score']}/100")
        print(f"Risk Category: {risk_assessment['risk_category']}")
        print(f"Anomaly Detected: {risk_assessment['is_anomaly']}")
        print(f"Confidence: {risk_assessment['confidence']}%")
        
        print("\nTop Risk Factors:")
        for factor in risk_assessment['risk_factors']:
            print(f"  - {factor['factor']}: {factor['impact']:.1f}% impact")
            print(f"    Recommendation: {factor['recommendation']}")
        
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    # Save models
    predictor.save_models()

if __name__ == "__main__":
    main()