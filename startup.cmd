@echo off
echo Starting startup script

REM Activate the virtual environment
call C:\home\site\wwwroot\venv\Scripts\activate.bat

echo Virtual environment activated

REM Start the Gunicorn server
gunicorn --bind 0.0.0.0:8000 lit.wsgi
