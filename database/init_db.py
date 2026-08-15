from database.connection import Base, engine
from database.models import Prediction


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")