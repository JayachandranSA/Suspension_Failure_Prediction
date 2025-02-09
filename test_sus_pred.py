import pytest
from sus_pred import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home page"""
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.text.strip() == "<h1> Suspension Component Health Prediction </h1>"

def test_predict(client):
    """Test the prediction endpoint"""
    test_data = {
        "vehicle_load_tons": 10.5,
        "road_type": 1,
        "shock_absorber_health": 0.8,
        "suspension_travel_mm": 50.2,
        "vehicle_age_years": 5
    }

    resp = client.post('/predict', json=test_data)
    assert resp.status_code == 200  # Ensure request is successful
    data = resp.get_json()
    
    assert "failure_prediction" in data
    assert "failure_probability" in data
    assert isinstance(data["failure_probability"], float)