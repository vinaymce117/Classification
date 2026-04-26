from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from src.model_loader import load_model

app = FastAPI()

model = load_model()

labels = ["Setosa", "Versicolor", "Virginica"]

class InputData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def home():
    return {"message": "API running with MLflow model"}

@app.post("/predict")
def predict(data: InputData):

    input_array = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    prediction = model.predict(input_array)

    pred = int(prediction[0])

    return {
        "prediction": pred,
        "label": labels[pred]
    }