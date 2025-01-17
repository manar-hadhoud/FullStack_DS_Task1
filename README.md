# FullStack_DS_Task1
# Iris Classification and Text Summarization Website 🌸✍️

This project is a full-stack web application that seamlessly integrates **Iris Flower Classification** and **Text Summarization** using cutting-edge machine learning models and large language models (LLMs) from Olama. It showcases the power of combining AI-driven solutions with modern web development to deliver an interactive and engaging experience.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project with Docker](#running-the-project-with-docker)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Frontend Usage](#frontend-usage)
- [Contributing](#contributing)
- [License](#license)

## Project Description

This web application features two powerful services:

1. **Iris Flower Classification**: A machine learning model classifies the species of an Iris flower based on user-provided measurements of petal length, petal width, sepal length, and sepal width.
   
2. **Text Summarization**: A generative AI model powered by Olama generates concise and meaningful summaries of text, allowing users to input long articles or paragraphs and get a shorter version.

The backend for both services is built using **FastAPI** for high performance, and the frontend is a responsive **React** application.

## Features 🚀

### 🌼 Iris Classification Backend
- FastAPI-based backend for classifying Iris flowers.
- Takes four input features: petal length, petal width, sepal length, and sepal width.
- Returns the predicted Iris species (Setosa, Versicolor, or Virginica).

### ✍️ Text Summarization Backend
- FastAPI-based backend that integrates with **Olama** for text summarization.
- Users can input text, and the backend generates a meaningful summary.
- Ideal for shortening long articles, research papers, or any other large chunks of text.

### 🎨 Frontend
- **React**-based user interface that allows users to interact with both services.
  - Input Iris flower measurements and view predictions.
  - Input long text for summarization and view the generated summaries.

## Tech Stack 💻

- **Backend**: FastAPI (for both Iris Classification and Text Summarization)
- **Frontend**: React (for creating a user-friendly UI)
- **Machine Learning**: Iris Flower Classification model
- **Large Language Models (LLMs)**: Olama API (for text summarization)
- **Docker**: Containerization for deployment

## Getting Started

### Prerequisites

Ensure you have the following tools installed on your system:

1. **Docker**: For building and running the project in containers. [Install Docker](https://www.docker.com/products/docker-desktop)
2. **Git**: For cloning the repository. [Install Git](https://git-scm.com/downloads)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/manar-hadhoud/FullStack_DS_Task1.git
   cd FullStack_DS_Task1

2. **Build and run the Docker container**:
   
   for backend:
   1. cd to/path/iris
   docker build -t fastapi-iris-app .
   docker run -d -p 8000:8000 --name iris-container fastapi-iris-app

   2. cd to/path/summerize
   docker build --no-cache -t summerization-app .
   docker run -d --name summerization-app --network host summerization-app

   for frontend:
   cd to/path/react/iris-predictor
   docker build -t react-app .
   docker run -d -p 3000:3000 --name react-app react-app


API Endpoints
🌼 /iris-classification - Iris Flower Classification
POST /iris-classification

This endpoint predicts the species of an Iris flower based on the provided measurements.
request body
{
  "petal_length": 5.1,
  "petal_width": 1.8,
  "sepal_length": 4.7,
  "sepal_width": 3.2
}

Response:
{
  "species": "Versicolor"
}

✍️ /summarize-text - Text Summarization
POST /summarize-text

This endpoint takes a long text and generates a summary.

Request Body:
{
  "text": "This is the text that will be summarized. It can be any length, and the model will generate a concise version of the content."
}

Response:
{
  "summary": "This is the summarized version of the provided text."
}
