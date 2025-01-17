from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from fastapi.middleware.cors import CORSMiddleware
import ollama
import requests


app = FastAPI()

# Allow all origins for CORS to resolve cross-origin issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can specify frontend origin)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model to define the input text format and validation
class InputText(BaseModel):
    text: str

    @staticmethod
    def validate_text(text: str):
        """Validates input text to ensure it's not empty, too short, or too long."""
        if not text.strip():
            raise ValueError("Input text cannot be empty.")
        if len(text) < 20:
            raise ValueError("Input text must be at least 20 characters long.")
        if len(text) > 10000:
            raise ValueError("Input text cannot exceed 10000 characters.")
        return text

    @classmethod
    def parse_text(cls, text: str):
        """Parses and validates the input text."""
        cls.validate_text(text)
        return {"text": text.strip()}


# Endpoint for summarizing text
@app.post("/summerize")
async def predict(input_text: InputText):
    """
    Summarizes the input text using the ollama model.
    
    Validates input text and communicates with the summarization model.
    Handles various exceptions and errors such as invalid input, timeout, etc.
    """

    try:
        # Validate and parse the input text
        parsed_text = InputText.parse_text(input_text.text)

        # Initialize the response as an empty string for streaming
        summary = ""

        # Call the Ollama API to summarize the input text
        try:
            response = ollama.generate(
                model="llama3.2:1b",
                prompt=f"Please summarize the following text: {parsed_text['text']}",
                stream=False  # Use non-streaming mode to handle the response synchronously
            )

            # Extract the summarized text from the response
            summary = response["response"]

        except requests.exceptions.Timeout:
            raise HTTPException(status_code=408, detail="The request to the summarization service timed out.")

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error occurred while making the request: {str(e)}")

        # Return the final summary generated
        return {"generated_text": summary}

    except ValueError as e:
        # Handle invalid input text and return a meaningful error message
        raise HTTPException(status_code=400, detail=str(e))

    except ValidationError as e:
        # Handle invalid input format (e.g., incorrect data type)
        raise HTTPException(status_code=422, detail="Invalid input format")

    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred1111: {str(e)}")

