# Dockerfile (Backend)
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements.txt from the root directory to the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code into the container
COPY ./backend /app/

# Set environment variables to prevent Django from prompting for input during migrations
ENV PYTHONUNBUFFERED=1

# Run migrations (makemigrations and migrate) before starting the server
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port (optional if you need to access it externally)
EXPOSE 8000

# Set the entrypoint to start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
