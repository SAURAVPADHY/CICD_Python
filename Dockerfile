# Use official Python 3.10 image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY . .

# Expose the default Flask port
EXPOSE 5000

# Run the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
