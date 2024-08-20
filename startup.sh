#!/bin/bash
echo "Starting startup script"

# Navigate to the project root directory where manage.py is located
cd "$(dirname "$0")" || { echo "Error: Application directory not found!"; exit 1; }

# Debugging: List contents of the venv directory
echo "Listing contents of venv/bin/"
ls -la ./venv/bin/

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

# Create a logs directory if it doesn't exist
LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

# Start the Gunicorn server with logging
echo "Starting Gunicorn server..."
exec  gunicorn --bind=0.0.0.0 --timeout 600 lit.wsgi \
    --access-logfile "$LOG_DIR/access.log" \
    --error-logfile "$LOG_DIR/error.log" \
    --log-level info
echo "Gunicorn server started..."
