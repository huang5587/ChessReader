FROM python:3.9

# Install system-level dependencies using apt
RUN apt-get update && apt-get install -y \
    pychess \
    stockfish \
    # Add other apt dependencies as needed \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy Python requirements file into the container
COPY requirements.txt .

# Install Python dependencies using pip
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# expose ports
ENV PORT=8080
EXPOSE 8080

# Define the command to run your Python application
CMD ["python", "server.py"]


