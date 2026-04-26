from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    res = client.get("/")
    assert res.status_code == 200

def test_predict():
    res = client.post("/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })

    assert res.status_code == 200
    assert "label" in res.json()