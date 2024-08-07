#!/bin/bash
echo "Starting startup script"

# Activate the virtual environment
source /home/site/wwwroot/venv/bin/activate

echo "Virtual environment activated"

# Start the Gunicorn server
gunicorn --bind 0.0.0.0:8000 lit.wsgi
