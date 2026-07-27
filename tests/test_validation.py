def test_negative_age(client) -> None:
    payload = {
        "age": -10,
        "sex": "male",
        "bmi": 25.0,
        "children": 0,
        "smoker": "no",
        "region": "northwest"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_invalid_gender(client) -> None:
    payload = {
        "age": 30,
        "sex": "abc",
        "bmi": 25.0,
        "children": 0,
        "smoker": "no",
        "region": "northwest"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_invalid_region(client) -> None:
    payload = {
        "age": 30,
        "sex": "male",
        "bmi": 25,
        "children": 0,
        "smoker": "no",
        "region": "india"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_negative_children(client) -> None:
    payload = {
        "age": 30,
        "sex": "male",
        "bmi": 25,
        "children": -1,
        "smoker": "no",
        "region": "northwest"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422