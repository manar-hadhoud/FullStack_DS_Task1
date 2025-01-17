# iris_api.py
from fastapi import APIRouter
from pydantic import BaseModel
import pickle
import asyncio

# Define the router
router = APIRouter()

# Load the trained model
with open('iris_model.sav', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open('class_mapping.pkl', 'rb') as f:
    class_mapping = pickle.load(f)

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@router.post("/predict")
async def predict_iris(features: IrisFeatures):
    
    # Predict the class using the loaded model
    #prediction = loaded_model.predict([input_features])
    try:
        # Extract features from the request
        input_features = [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width,
        ]

        # Predict the class using the loaded model
        #prediction = await asyncio.to_thread(loaded_model.predict, [input_features])
        prediction = loaded_model.predict([input_features])

        # Map the predicted class index to the class name
        predicted_class_name = class_mapping[prediction[0]]

        # Return the result as a response
        return {"predicted_class": predicted_class_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

