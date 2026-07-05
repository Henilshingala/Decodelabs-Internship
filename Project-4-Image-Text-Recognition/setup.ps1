Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Project 4 Setup - Image/Text Recognition" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.12+ and try again." -ForegroundColor Red
    exit 1
}

Write-Host "[2/4] Setting up virtual environment..." -ForegroundColor Yellow
if (!(Test-Path "venv")) {
    python -m venv venv
}
& .\venv\Scripts\Activate.ps1

Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "[4/4] Downloading model files..." -ForegroundColor Yellow
python download_models.py

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Note: For OCR to work, you MUST install Tesseract OCR on your system." -ForegroundColor Magenta
Write-Host "Download it from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Magenta
Write-Host ""
Write-Host "To run the scripts, make sure your virtual environment is activated:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  python object_detection.py" -ForegroundColor Yellow
Write-Host "  python ocr.py" -ForegroundColor Yellow
Write-Host ""
