from flask import Flask, request, jsonify
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

# Load Model with Error Handling
model_path = "suspension_model.pkl"

if os.path.exists(model_path):
    try:
        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)
    except Exception as e:
        model = None
        print(f"Error loading model: {e}")
else:
    model = None
    print("Model file not found!")

# API Endpoints
@app.route('/')
def home():
    return "<h1>Suspension Component Health Prediction</h1>"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model could not be loaded!"}), 500

    sus_data = request.get_json()

    try:
        vehicle_load_tons = float(sus_data.get('vehicle_load_tons', 0))
        road_type = int(sus_data.get('road_type', 0))
        shock_absorber_health = float(sus_data.get('shock_absorber_health', 0))
        suspension_travel_mm = float(sus_data.get('suspension_travel_mm', 0))
        vehicle_age_years = float(sus_data.get('vehicle_age_years', 0))

        features = [[vehicle_load_tons, road_type, shock_absorber_health, suspension_travel_mm, vehicle_age_years]]

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        status = "Failure Likely" if prediction == 1 else "No Failure Expected"

        return jsonify({
            "failure_prediction": status,
            "failure_probability": round(float(probability), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)