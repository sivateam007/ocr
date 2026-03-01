#!/usr/bin/env bash
# Update packages and install Tesseract with Tamil language support
apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-tam
# Install Python dependencies
pip install -r requirements.txt