from flask import Flask,request,jsonify, render_template
import pickle

#Master Varible + Controls entire application
app =  Flask(__name__)

#Load Model
model_file = open("suspension_model.pkl","rb")
model = pickle.load(model_file)

#API Endpoints
@app.route('/')

def home():
    return"<h1> Suspesion Component Health prediction </h1>"

@app.route('/predict', methods = ['POST'])

def predict():
    sus_data = request.get_json()

    try:

        vehicle_load_tons = float(sus_data['vehicle_load_tons'])
        road_type = int(sus_data['road_type'])
        shock_absorber_health = float(sus_data['shock_absorber_health'])
        suspension_travel_mm = float(sus_data['suspension_travel_mm'])
        vehicle_age_years = float(sus_data['vehicle_age_years'])
        
        features = [vehicle_load_tons, road_type, shock_absorber_health, suspension_travel_mm, vehicle_age_years]
    
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]

        status = "Failure Likely" if prediction == 1 else "No Failure Expected"

        # return {"Suspension component is",status}
        return jsonify({"failure_prediction": status,"failure_probability": round(float(probability), 2)})
    except Exception as e:
        return jsonify ({"error" : str(e)})
    
if __name__ == '__main__':
    app.run(debug=False)