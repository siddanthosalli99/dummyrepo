from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cement: Mapped[float] = mapped_column(Float)
    blast_furnace_slag: Mapped[float] = mapped_column(Float)
    fly_ash: Mapped[float] = mapped_column(Float)
    water: Mapped[float] = mapped_column(Float)
    superplasticizer: Mapped[float] = mapped_column(Float)
    coarse_aggregate: Mapped[float] = mapped_column(Float)
    fine_aggregate: Mapped[float] = mapped_column(Float)
    age: Mapped[float] = mapped_column(Float)
    prediction: Mapped[float] = mapped_column(Float)