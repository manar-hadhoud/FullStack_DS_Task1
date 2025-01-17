# main.py
from fastapi import FastAPI
from Rout_iris import router as iris_router
from Rout_summerize import router as summarization_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers in the app
app.include_router(iris_router, prefix="/iris", tags=["Iris Prediction"])
app.include_router(summarization_router, prefix="/summarization", tags=["Text Summarization"])

@app.get("/")
def root():
    return {"message": "Welcome to the API. Use /iris/predict for classification and /summarization/summarize for text summarization."}
