import joblib
from typing import Literal

import pandas as pd
import pickle
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from prometheus_fastapi_instrumentator import Instrumentator

# Load Model

model = joblib.load("model.pkl")

# Create FastAPI app

app: FastAPI = FastAPI(
    title="Insurance Charges Prediction API",
    version="1.0.0"
)

# Pydantic

class InsuranceData(BaseModel):
    age: int = Field(..., ge=18, le=100)
    sex: Literal["male", "female"]
    bmi: float = Field(..., ge=10.0, le=60.0)
    children: int = Field(..., ge=0, le=10)
    smoker: Literal["yes", "no"]
    region: Literal[
        "northeast",
        "northwest",
        "southeast",
        "southwest"
    ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 35,
                "sex": "male",
                "bmi": 27.5,
                "children": 2,
                "smoker": "no",
                "region": "southwest"
            }
        }
    )

# Home Endpoint

@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Insurance Prediction API is running."
    }

# Prediction Endpoint

@app.post("/predict")
def predict(data: InsuranceData) -> dict[str, float]:

    input_df: pd.DataFrame = pd.DataFrame([data.model_dump()])

    prediction: list[float] = model.predict(input_df)

    predicted_charge: float = float(prediction[0])

    return {
        "predicted_charges": round(predicted_charge, 2)
    }

# prometheus

Instrumentator().instrument(app).expose(app)