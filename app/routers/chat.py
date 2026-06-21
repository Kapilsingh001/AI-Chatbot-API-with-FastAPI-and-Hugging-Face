# app/routers/chat.py

# We now also import HTTPException to return clean errors.
from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse
from app.models.chatbot import generate_reply

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message

    # Wrap the risky model call in try/except so a crash becomes a clean error.
    try:
        bot_reply = generate_reply(user_message)
    except Exception as e:
        # If anything goes wrong while generating, return a controlled 500 error
        # with a helpful message instead of leaking a raw traceback to the client.
        raise HTTPException(
            status_code=500,
            detail="Failed to generate a reply. Please try again."
        )

    return ChatResponse(reply=bot_reply)


# from fastapi import APIRouter → the tool for grouping routes.
# from app.schemas import ... → our two contracts. (Note the import path app.schemas — this works because of those __init__.py files making app a package! 🧩)
# from app.models.chatbot import generate_reply → the brain function.
# router = APIRouter() → creates the mini-app.
# @router.post("/chat", response_model=ChatResponse) → a decorator registering the function below as a POST handler at /chat. (A decorator is the @something line that "attaches behavior" to the function under it.)
# def chat(request: ChatRequest): → the handler. The request: ChatRequest hint triggers auto-validation.
# return ChatResponse(reply=bot_reply) → returns the promised shape; FastAPI JSON-ifies it.

# from fastapi import APIRouter, HTTPException → added HTTPException.
# try: → "attempt this risky thing."
# except Exception as e: → "if any error happens, catch it." (as e names the error object — useful for logging later.)
# raise HTTPException(status_code=500, detail=...) → returns a clean 500 with a friendly message. The client now gets {"detail": "Failed to generate a reply. Please try again."} instead of a crash. ✅
