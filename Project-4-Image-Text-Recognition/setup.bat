@echo off
echo ==========================================
echo Project 4 Setup - Image/Text Recognition
echo ==========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.12+ and try again.
    exit /b 1
)

echo [2/4] Setting up virtual environment...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo [4/4] Downloading model files...
python download_models.py

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo Note: For OCR to work, you MUST install Tesseract OCR on your system.
echo Download it from: https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo To run the scripts, make sure your virtual environment is activated:
echo   venv\Scripts\activate
echo   python object_detection.py
echo   python ocr.py
echo.
pause
