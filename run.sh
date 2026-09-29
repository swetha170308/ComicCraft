#!/usr/bin/env bash
# ComicCraft Startup Script

echo "=========================================================="
echo " Starting ComicCraft - AI Comic Story Creator (FastAPI)    "
echo "=========================================================="

# Check if virtual environment exists
if [ -d "env" ]; then
    echo "Activating virtual environment..."
    source env/bin/activate
fi

# Ensure output directories exist
mkdir -p static/panels static/exports static/fonts

echo "Launching Uvicorn server on http://127.0.0.1:8000..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
