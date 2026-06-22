# Start from an official lightweight Python image as our base.
# "slim" = a smaller version with less bloat.
FROM python:3.11-slim

# Set the working directory inside the container. All later commands run here.
WORKDIR /app

# Copy ONLY requirements.txt first (not all code yet).
# This is a Docker best practice: if code changes but deps don't,
# Docker reuses the cached install layer = faster rebuilds.
COPY requirements.txt .

# Install the Python dependencies inside the container.
# --no-cache-dir keeps the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of our application code into the container.
COPY ./app ./app

# Copy the frontend (static/index.html) so the chat UI is available inside the container.
COPY ./static ./static

# Tell Docker the container will listen on port 8000.
EXPOSE 8000

# The command that runs when the container starts.
# Note: host must be 0.0.0.0 (not 127.0.0.1) so it's reachable from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
