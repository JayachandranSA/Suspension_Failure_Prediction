from flask import Flask, request, jsonify
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the model safely
try:
    with open("suspension_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    print("✅ Model loaded successfully!")  # Debugging print statement
except Exception as e:
    print(f"❌ Error loading model: {e}")  # Debugging print statement
    model = None  # Handle model loading failure

# API Endpoints
@app.route('/')
def home():
    return "<h1> Suspension Component Health Prediction </h1>"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model failed to load."}), 500  # Return error if model is missing

    try:
        sus_data = request.get_json()

        # Ensure all required keys are in the request
        required_keys = ["vehicle_load_tons", "road_type", "shock_absorber_health", "suspension_travel_mm", "vehicle_age_years"]
        for key in required_keys:
            if key not in sus_data:
                return jsonify({"error": f"Missing key: {key}"}), 400

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
        print(f"❌ Error in prediction: {e}")  # Log error
        return jsonify({"error": str(e)}), 500  # Return error response


# Run Flask app
if __name__ == '__main__':
    app.run(debug=False)