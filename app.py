import joblib
import pandas as pd
from fastapi import Depends, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from typing import Literal

from database.connection import get_db
from database.models import Prediction


model = joblib.load("model.pkl")


app: FastAPI = FastAPI(
    title="Insurance Charges Prediction API",
    version="1.0.0",
)


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
        "southwest",
    ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 35,
                "sex": "male",
                "bmi": 27.5,
                "children": 2,
                "smoker": "no",
                "region": "southwest",
            }
        }
    )


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Insurance Prediction API is running."
    }


@app.post("/predict")
def predict(
    data: InsuranceData,
    db: Session = Depends(get_db),
) -> dict[str, float]:

    input_df: pd.DataFrame = pd.DataFrame([data.model_dump()])

    prediction: list[float] = model.predict(input_df)

    predicted_charge: float = float(prediction[0])

    db_prediction = Prediction(
        age=data.age,
        sex=data.sex,
        bmi=data.bmi,
        children=data.children,
        smoker=data.smoker,
        region=data.region,
        prediction=predicted_charge,
    )

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return {
        "predicted_charges": round(predicted_charge, 2)
    }


Instrumentator().instrument(app).expose(app)