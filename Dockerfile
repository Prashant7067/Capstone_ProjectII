# Use the official Python image as a base
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Create necessary folders if they don't exist
RUN mkdir -p uploads static/compressed static/enhanced static/fused

# Expose the port your app runs on
EXPOSE 8081

RUN pip install -r requirements.txt

# Define the command to run your application
CMD ["python", "main.py"]