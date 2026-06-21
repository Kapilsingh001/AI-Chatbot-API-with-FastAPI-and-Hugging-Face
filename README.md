# AI Chatbot API 🤖

A simple chatbot API built with **FastAPI** and **Hugging Face Transformers**, using the pre-trained `microsoft/DialoGPT-small` model.

## Features
- REST API endpoint (`POST /chat`) to chat with the bot
- Automatic interactive documentation (Swagger UI)
- Input validation with Pydantic
- Graceful error handling

## Tech Stack
- **FastAPI** – web framework
- **Uvicorn** – ASGI server
- **Transformers** – Hugging Face model loading
- **PyTorch** – deep learning engine

## Setup & Installation

1. Clone the repository (or download the files).
2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
