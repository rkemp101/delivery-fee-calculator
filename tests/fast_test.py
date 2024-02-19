from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_api_response():
    response = client.get("/")
    assert response.status_code == 200

def test_api_invalid_time():
    payload = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T15:00:00"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 400

def test_api_standard_order():
    payload = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T15:00:00Z"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}

def test_api_standard_order_free_delivery():
    payload = {"cart_value": 20000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T15:00:00Z"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 0}

def test_api_standard_order_max_fee():
    payload = {"cart_value": 13000, "delivery_distance": 4000, "number_of_items": 26, "time": "2024-01-15T15:00:00Z"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 1500}

def test_api_peak_order():
    payload = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T15:00:00Z"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 852}

def test_api_peak_order_free_delivery():
    payload = {"cart_value": 20000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T15:00:00Z"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 0}

def test_api_peak_order_max_fee():
    payload = {"cart_value": 6500, "delivery_distance": 4000, "number_of_items": 13, "time": "2024-01-19T15:00:00Z"}
    response = client.post("/calculate-delivery-fee/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 1500}
