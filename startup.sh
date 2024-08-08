#!/bin/bash
echo "Starting startup script"

# Navigate to the project root directory where manage.py is located
cd /home/site/wwwroot || { echo "Error: Application directory not found!"; exit 1; }

# Alternatively, for local development, you could use:
# cd /path/to/your/project/root || { echo "Error: Application directory not found!"; exit 1; }

# Activate the virtual environment
if [ -f ./venv/bin/activate ]; then
    source ./venv/bin/activate
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

# Start the Gunicorn server with the correct WSGI module
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 lit.wsgi
