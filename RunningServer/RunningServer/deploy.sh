#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment..."

# Navigate to your project directory
cd ./RunningServer/RunningServer/

# Pull latest changes
git pull origin main

# Activate virtual environment
source /path/to/your/virtualenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "Deployment successful!"