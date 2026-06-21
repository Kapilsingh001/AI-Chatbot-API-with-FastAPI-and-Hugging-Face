# # app/main.py

# # Import the FastAPI class — the heart of our application.
# from fastapi import FastAPI

# # Import the router we just built in routers/chat.py.
# from app.routers import chat

# # Create the FastAPI application instance.
# # The title shows up in the auto-generated docs (Phase 7).
# app = FastAPI(title="AI Chatbot API")


# # A simple "health check" route at the root URL "/".
# # Useful to quickly confirm the server is alive.
# @app.get("/")
# def root():
#     return {"message": "Chatbot API is running!"}


# # Plug the chat router into our main app.
# # Now all routes defined in chat.py (like /chat) become part of the API.
# app.include_router(chat.router)



# # from fastapi import FastAPI → the main application class.
# # from app.routers import chat → imports our router module.
# # app = FastAPI(title="AI Chatbot API") → creates the app; title labels the docs.
# # @app.get("/") → a GET route at the root, returning a simple "I'm alive" message. (GET is right here — we're just reading a status.)
# # app.include_router(chat.router) → the "plug it in" step. chat.router is the router object from chat.py.


# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import chat
from app.models.chatbot import load_model


# A "lifespan" function runs setup code BEFORE the app starts serving,
# and (optionally) cleanup code AFTER it shuts down.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup: runs once when the server starts ---
    load_model()
    yield            # the app runs while "paused" here
    # --- shutdown: code after yield runs when server stops (none needed yet) ---


# Attach the lifespan to our app so load_model() runs on startup.
app = FastAPI(title="AI Chatbot API", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}


app.include_router(chat.router)


# 🟡 Q2 — Purpose & timing of lifespan
# "lifespan helps in starting the model once for multiple use without loading again and again" → ✅ Correct! That's the purpose nailed.

# "the code before yield runs when we hit an api request" → 🔴 Not quite.

# The code before yield runs once, at server startup — before any request arrives. Not per-request!