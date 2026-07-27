import joblib
import pandas as pd


model = joblib.load("model.pkl")


def test_model_prediction() -> None:
    sample = pd.DataFrame({
        "age": [40],
        "sex": ["female"],
        "bmi": [28.5],
        "children": [2],
        "smoker": ["no"],
        "region": ["southwest"]
    })

    prediction = model.predict(sample)

    assert len(prediction) == 1
    assert prediction[0] > 0


def test_model_returns_numeric() -> None:
    sample = pd.DataFrame({
        "age": [30],
        "sex": ["male"],
        "bmi": [24.0],
        "children": [1],
        "smoker": ["yes"],
        "region": ["southeast"]
    })

    prediction = model.predict(sample)

    assert isinstance(float(prediction[0]), float)