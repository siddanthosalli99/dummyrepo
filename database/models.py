from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String)
    bmi: Mapped[float] = mapped_column(Float)
    children: Mapped[int] = mapped_column(Integer)
    smoker: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    prediction: Mapped[float] = mapped_column(Float)