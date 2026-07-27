def test_home(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Insurance Prediction API is running."
    }


def test_prediction(client) -> None:
    payload = {
        "age": 25,
        "sex": "male",
        "bmi": 26.5,
        "children": 1,
        "smoker": "no",
        "region": "northwest"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "predicted_charges" in data
    assert isinstance(data["predicted_charges"], float)