# app/schemas.py

# Import Field too — it lets us add validation rules to fields.
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    # message is required (...) and must be at least 1 character long.
    # We can also strip-check with min_length on the trimmed value later if needed.
    message: str = Field(..., min_length=1, description="The user's message to the chatbot")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="The chatbot's generated reply")



# from pydantic import BaseModel → brings in the base class that powers validation.
# class ChatRequest(BaseModel): → defines our input schema. The (BaseModel) part means "inherit all of Pydantic's validation machinery."
# message: str → declares one required field named message of type str (string/text). The : str is a type hint — Pydantic enforces it at runtime (unlike normal Python type hints, which are just suggestions).
# class ChatResponse(BaseModel): with reply: str → our output schema: we always return a reply string.


# from pydantic import BaseModel, Field → added Field.
# Field(..., min_length=1, ...) → ... = required; min_length=1 = reject empty strings; description=... = shows up in your Swagger docs! 📖
# This makes {"message": ""} automatically fail with 422. Try it in /docs after! 🧪