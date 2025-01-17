from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import traceback  # For detailed error logging
from dotenv import load_dotenv
import os

app = FastAPI()

# Load .env file
load_dotenv()

# Load file paths from environment variables
MODEL_PATH = os.getenv("MODEL_PATH")  # Default to 'iris_model.sav'
CLASS_MAPPING_PATH = os.getenv("CLASS_MAPPING_PATH")


# Add CORS middleware to handle requests from different origins (e.g., React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (set specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Load the trained model
try:
    with open(MODEL_PATH, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
except FileNotFoundError:
    raise RuntimeError("Model file not found. Ensure 'iris_model.sav' is in the correct location.")
except Exception as e:
    raise RuntimeError(f"Error loading the model: {e}")



# Load the class mapping to map predictions to human-readable labels
try:
    with open(CLASS_MAPPING_PATH, 'rb') as f:
        class_mapping = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("Class mapping file not found. Ensure 'class_mapping.pkl' is in the correct location.")
except Exception as e:
    raise RuntimeError(f"Error loading class mapping: {e}")



# Define the input schema for the prediction endpoint
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float



# Welcome endpoint for initial API interaction
@app.get("/")
def root():
    return {"message": "Welcome to the Iris Prediction API"}



# Prediction endpoint to classify Iris flower species
@app.post("/predict")
async def predict_iris(features: IrisFeatures):
    try:
        # Extract input features from the request payload
        input_features = [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width,
        ]

        # Check if the model is loaded properly
        if not loaded_model:
            raise HTTPException(status_code=500, detail="Model is not loaded properly.")

        # Check if the class mapping is loaded properly
        if not class_mapping:
            raise HTTPException(status_code=500, detail="Class mapping is not loaded properly.")

        # Make a prediction using the model
        prediction = loaded_model.predict([input_features])

        # Convert the predicted class index to a class name
        predicted_class_name = class_mapping[prediction[0]]

        # Return the predicted class name
        return {"predicted_class": predicted_class_name}

    except ValueError as ve:
        # Handle invalid input data
        print("ValueError:", ve)
        raise HTTPException(status_code=400, detail="Invalid input data format.")

    except KeyError as ke:
        # Handle issues with the class mapping
        print("KeyError:", ke)
        raise HTTPException(
            status_code=500,
            detail="Error mapping the prediction to a class name. Please check the class mapping file.",
        )

    except Exception as e:
        # Handle unexpected errors and log the traceback
        print("Unexpected error:", traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )
