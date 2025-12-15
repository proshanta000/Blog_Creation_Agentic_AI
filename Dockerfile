# Stage 1: Use a reliable Python base image
# We use 'slim' for a smaller, faster container image.
FROM python:3.11-slim

# Set the working directory inside the container
# All commands will be run relative to this directory (/app)
WORKDIR /app

# 1. Install Dependencies
# Copy the requirements file first to take advantage of Docker's build cache.
COPY requirements.txt .

# Install Python packages. The --no-cache-dir flag keeps the image small.
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy Application Code
# Copy all remaining files from your repository's root directory (where the Dockerfile is)
# into the container's /app directory. This copies:
# - app.py
# - src/
# - templates/
# - uiconfigfile.ini (if present)
COPY . .

# 3. Final Command to Run the Application
# CMD defines the command to execute when the container starts.
# We explicitly run Uvicorn on host 0.0.0.0 and port 7860, as required by Hugging Face Spaces.
# 'app:app' refers to the 'app' object inside the 'app.py' file.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]