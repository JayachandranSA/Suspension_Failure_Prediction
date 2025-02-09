from flask import Flask, request, jsonify
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the model safely
try:
    with open("suspension_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Handle if the model fails to load

# API Endpoints
@app.route('/')
def home():
    return "<h1> Suspension Component Health Prediction </h1>"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model failed to load."}), 500

    sus_data = request.get_json()
    try:
        # Extract features
        vehicle_load_tons = float(sus_data['vehicle_load_tons'])
        road_type = int(sus_data['road_type'])
        shock_absorber_health = float(sus_data['shock_absorber_health'])
        suspension_travel_mm = float(sus_data['suspension_travel_mm'])
        vehicle_age_years = float(sus_data['vehicle_age_years'])

        features = [[vehicle_load_tons, road_type, shock_absorber_health, suspension_travel_mm, vehicle_age_years]]

        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        # Determine status
        status = "Failure Likely" if prediction == 1 else "No Failure Expected"

        return jsonify({
            "failure_prediction": status,
            "failure_probability": round(float(probability), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run Flask app
if __name__ == '__main__':
    app.run(debug=False)