# MLOps-CI-CD
The repository for the MLOps CI/CD homeworks

# ML Inference Docker Project

## Setup
```bash
bash install_dev_tools.sh

## Build Docker images
docker build -f Dockerfile.fat -t ml-fat .
docker build -f Dockerfile.slim -t ml-slim .

## Run inference
docker run --rm ml-fat python inference.py example.jpg
docker run --rm ml-slim python inference.py example.jpg

