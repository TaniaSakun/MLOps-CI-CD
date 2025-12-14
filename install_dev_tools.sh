#!/bin/bash

LOG_FILE="install.log"

echo "=== Dev/ML Environment Setup ===" | tee -a $LOG_FILE

# --- Check and install Docker ---
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..." | tee -a $LOG_FILE
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl enable --now docker
else
    echo "Docker is already installed" | tee -a $LOG_FILE
fi

# --- Check and install Docker Compose ---
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose not found. Installing..." | tee -a $LOG_FILE
    sudo apt install -y docker-compose
else
    echo "Docker Compose is already installed" | tee -a $LOG_FILE
fi

# --- Check Python >=3.9 ---
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION=3.9
if [[ $(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc) -eq 1 ]]; then
    echo "Python < 3.9 detected. Installing Python 3.9..." | tee -a $LOG_FILE
    sudo apt install -y python3.9 python3.9-venv python3.9-dev
else
    echo "Python version is $PYTHON_VERSION" | tee -a $LOG_FILE
fi

# --- Check pip ---
if ! command -v pip3 &> /dev/null; then
    echo "pip not found. Installing..." | tee -a $LOG_FILE
    sudo apt install -y python3-pip
else
    echo "pip is already installed" | tee -a $LOG_FILE
fi

# --- Python libraries ---
echo "Installing Python libraries: torch, torchvision, pillow..." | tee -a $LOG_FILE
pip3 install --upgrade pip | tee -a $LOG_FILE
pip3 install torch torchvision pillow | tee -a $LOG_FILE

echo "=== Setup Complete ===" | tee -a $LOG_FILE
