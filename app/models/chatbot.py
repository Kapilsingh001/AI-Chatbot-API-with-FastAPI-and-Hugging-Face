# # app/models/chatbot.py

# # Import the two "Auto" helper classes from the transformers library.
# # AutoTokenizer        -> loads the text<->numbers translator
# # AutoModelForCausalLM -> loads the text-generating model
# from transformers import AutoTokenizer, AutoModelForCausalLM

# # The name of the model on Hugging Face. This exact string is its "address".
# MODEL_NAME = "microsoft/DialoGPT-small"

# # Load the tokenizer that matches this model.
# # On first run this downloads & caches it; later runs load from cache.
# print("Loading tokenizer...")
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# # Load the model itself (the neural network with all its learned weights).
# print("Loading model...")
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# print("Model loaded successfully!")


# # A function that takes a user's message (text) and returns the bot's reply (text).
# def generate_reply(user_message: str) -> str:
#     # STEP 1 — ENCODE: turn the user's text into token IDs the model understands.
#     # Calling tokenizer(...) directly returns BOTH the input_ids AND the attention_mask.
#     # We add the "end of string" token so the model knows the user's turn ended.
#     # return_tensors="pt" means "give me PyTorch tensors" (pt = PyTorch).
#     inputs = tokenizer(
#         user_message + tokenizer.eos_token,
#         return_tensors="pt"
#     )

#     # STEP 2 — GENERATE: ask the model to produce a reply.
#     # We pass attention_mask so the model doesn't have to guess which tokens are real.
#     # max_length caps how long the whole conversation (input + reply) can get.
#     # pad_token_id tells the model what "padding" looks like (silences a warning).
#     output_ids = model.generate(
#         inputs["input_ids"],
#         attention_mask=inputs["attention_mask"],
#         max_length=1000,
#         pad_token_id=tokenizer.eos_token_id
#     )

#     # STEP 3 — DECODE: the output includes our input + the reply glued together.
#     # We slice off the input part to keep ONLY the reply, then decode the numbers
#     # back into readable text.
#     reply = tokenizer.decode(
#         output_ids[:, inputs["input_ids"].shape[-1]:][0],
#         skip_special_tokens=True
#     )

#     return reply


# # This block ONLY runs if we execute this file directly (python app/models/chatbot.py).
# # It will NOT run when the file is imported by FastAPI later.
# # It's our quick way to TEST the brain in isolation.
# if __name__ == "__main__":
#     print(generate_reply("I love pizza."))



# app/models/chatbot.py

from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "microsoft/DialoGPT-small"

# We declare these as None at first — they'll be filled in when we call load_model().
# This avoids loading the model just because the file got imported.
tokenizer = None
model = None


# A function that loads the model into the module-level variables above.
# We call this ONCE, on app startup (see main.py), instead of at import time.
def load_model():
    global tokenizer, model            # tell Python we're assigning the outer variables
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    print("Model loaded successfully!")


def generate_reply(user_message: str) -> str:
    # Safety check: if the model wasn't loaded, fail clearly instead of confusingly.
    if model is None or tokenizer is None:
        raise RuntimeError("Model not loaded. Call load_model() first.")

    inputs = tokenizer(
        user_message + tokenizer.eos_token,
        return_tensors="pt"
    )

    output_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    reply = tokenizer.decode(
        output_ids[:, inputs["input_ids"].shape[-1]:][0],
        skip_special_tokens=True
    )

    return reply


# tokenizer = None / model = None → we declare them but don't load yet. Importing this file is now cheap and side-effect-free. ✅
# def load_model(): → loading is now an action we trigger on purpose, not an import accident.
# global tokenizer, model → inside a function, assigning to a module-level variable requires global, or Python would create a new local variable instead. (Good Python lesson! 🐍)
# The if model is None guard in generate_reply → clear error if someone forgets to load. Defensive programming. 🛡️
# I removed the if __name__ == "__main__": test block since we now load via the app. (You can keep a test block that calls load_model() first if you like.)