from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel , ValidationError
import ollama
import requests
import asyncio


router = APIRouter()

# Pydantic model to define the input format
class InputText(BaseModel):
    text: str

    @staticmethod
    def validate_text(text: str):
        if not text.strip():
            raise ValueError("Input text cannot be empty.")
        if len(text) < 20:
            raise ValueError("Input text must be at least 20 characters long.")
        if len(text) > 10000:
            raise ValueError("Input text cannot exceed 500 characters.")
        return text

    @classmethod
    def parse_text(cls, text: str):
        cls.validate_text(text)
        return {"text": text.strip()}



# Define the prediction endpoint
@router.post("/summerize")
async def predict(input_text: InputText):
    try:
        # Validate and parse the input text
        parsed_text = InputText.parse_text(input_text.text)

        # Run the summarization task asynchronously and await the result
        summary = await generate_summary(parsed_text['text'])

        # Return the summary as a response
        return {"generated_text": summary}
    
    except ValueError as e:
        # Handle invalid input text and return a meaningful error message
        raise HTTPException(status_code=400, detail=str(e))

    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Invalid input format")

    except TimeoutError:
        raise HTTPException(status_code=408, detail="The request to the summarization service timed out.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def generate_summary(text: str):
    try:
        # Call the Ollama service to generate the summary
        response = await asyncio.to_thread(ollama.generate, model="llama3.2:1b", prompt=f"Please summarize the following text: {text}", stream=True)

        # Collect and combine the response data
        summary = ""
        for chunk in response:
            data = chunk.get("response", "")
            summary += data

        return summary

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="The request to the summarization service timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during summarization: {str(e)}")
