FROM python:3.11-slim-buster

# Install dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the port your application will listen on
EXPOSE 5000

# Command to run your application
CMD ["python", "main.py"]