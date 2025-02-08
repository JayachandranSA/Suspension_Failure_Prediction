import pytest
from sus_pred import app

#proxy for live server
@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.text == "<h1> Suspesion Component Health prediction </h1>"


def test_predict(client):
    test_data = {
                "vehicle_load_tons" : 38,
                "road_type" : 2,
                "shock_absorber_health" : 89,
                "suspension_travel_mm" : 40,
                "vehicle_age_years" : 3}
    resp =client.post('/predict',json = test_data)
    assert resp.status_code == 200
    resp.json == {"Failure Likely"}