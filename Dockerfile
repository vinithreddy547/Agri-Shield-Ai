# Use lightweight official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for compiling python packages if any
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose standard Streamlit port
EXPOSE 8501

# Run healthcheck to verify container is active
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the dashboard
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
