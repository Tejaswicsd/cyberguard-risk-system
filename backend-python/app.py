import os
import sys
from cyber_risk_predictor import CyberRiskPredictor

def main():
    print("🚀 CyberGuard Risk Assessment System Starting...")
    
    # Initialize and train ML models
    predictor = CyberRiskPredictor()
    predictor.train_models()
    
    # Save models for API use
    predictor.save_models()
    
    print("✅ System initialized successfully!")
    print("🔥 Starting Flask API server...")
    
    # Start API server
    os.system("python api_server.py")

if __name__ == "__main__":
    main()