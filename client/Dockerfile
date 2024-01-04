FROM python:3.9

WORKDIR /client

# Copy your application files into the container
COPY . /client

# Expose the port for the HTTP server

ENV PORT=3000
EXPOSE 3000

# Start the Python HTTP server
CMD ["python", "-m", "http.server", "3000"]
