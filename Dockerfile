# Use a lean and lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code
COPY . .

# Expose the port that gunicorn will run on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "run:app"]