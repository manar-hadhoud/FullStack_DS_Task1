# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

RUN pip install python-dotenv

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . /app/

# Expose the port the app runs on 8000
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "iris_api:app", "--host", "0.0.0.0", "--port", "8000"]
