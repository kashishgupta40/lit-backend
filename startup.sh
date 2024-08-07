#!/bin/bash
echo "Starting startup script"

# Activate the virtual environment
if [ -f /home/site/wwwroot/venv/bin/activate ]; then
    source /home/site/wwwroot/venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Error: Virtual environment activation script not found!"
    exit 1
fi

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Error: gunicorn is not installed!"
    exit 1
fi

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 lit.wsgi

