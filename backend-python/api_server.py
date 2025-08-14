from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from cyber_risk_predictor import CyberRiskPredictor

app = Flask(__name__)
CORS(app)

# Initialize risk predictor
predictor = CyberRiskPredictor()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "cyber-risk-api"})

@app.route('/api/assess-entity', methods=['POST'])
def assess_entity():
    try:
        entity_data = request.json
        risk_assessment = predictor.predict_risk(entity_data)
        recommendations = predictor.generate_recommendations(risk_assessment)
        
        response = {
            "entity_id": entity_data.get('entity_id', 'unknown'),
            "risk_assessment": risk_assessment,
            "recommendations": recommendations,
            "timestamp": str(datetime.now())
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bulk-assess', methods=['POST'])
def bulk_assess():
    try:
        entities = request.json.get('entities', [])
        results = {}
        
        for entity in entities:
            entity_id = entity.get('entity_id', 'unknown')
            risk_assessment = predictor.predict_risk(entity)
            recommendations = predictor.generate_recommendations(risk_assessment)
            
            results[entity_id] = {
                "risk_assessment": risk_assessment,
                "recommendations": recommendations
            }
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)