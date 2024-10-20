# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Install system dependencies for MySQL client and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config

# Step 4: Set the working directory in the container
WORKDIR /app

# Step 5: Copy the current directory contents into the container at /app
COPY . /app/

# Step 6: Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 7: Collect static files for Django
RUN python manage.py collectstatic --noinput

# Step 8: Expose port 8000 to the outside world
EXPOSE 8000

# Step 9: Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]