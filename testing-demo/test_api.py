import requests

BASE_URL = "http://127.0.0.1:5000"

def test_get_all_customers():
    response = requests.get(f"{BASE_URL}/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customer_by_id():
    response = requests.get(f"{BASE_URL}/customers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data

def test_create_customer():
    payload = {
        "name": "Charlie",
        "address": "Da Nang",
        "phone": "0909090909"
    }
    response = requests.post(f"{BASE_URL}/customers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charlie"

def test_update_customer():
    payload = {
        "name": "Alice Updated",
        "address": "Hanoi",
        "phone": "0123456789"
    }
    response = requests.put(f"{BASE_URL}/customers/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice Updated"

def test_delete_customer():
    response = requests.delete(f"{BASE_URL}/customers/2")
    assert response.status_code == 204
