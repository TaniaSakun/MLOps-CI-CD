# MLOps-CI-CD: ML Inference Docker Project

This repository contains the homework for MLOps CI/CD lessons. It demonstrates how to containerize a PyTorch model using Docker, including a "fat" and a "slim" image, and run inference on test images.

---

## Project Structure
```
lesson-3/
├── inference.py # Script for model inference
├── export_model.py # Script to export TorchScript model
├── model.pt # TorchScript model
├── Dockerfile.fat # "Fat" Docker image
├── Dockerfile.slim # "Slim" Docker image (optimized)
├── install_dev_tools.sh # Bash script to prepare environment
├── test_images/ # Folder with test images
├── imagenet_classes.txt # List of ImageNet classes
├── comparison.txt # Comparison of fat vs slim images
└── README.md
```

---

## Setup Environment

Run the setup script to install Docker, Docker Compose, Python ≥3.9, and necessary Python libraries:

```bash
bash install_dev_tools.sh
```

This script will check for existing installations and install any missing dependencies. After execution, Docker, Python, pip, and required Python libraries (torch, torchvision, pillow) will be available.

## Build Docker Images

```bash
# Fat image
docker build -f Dockerfile.fat -t ml-fat .

# Slim image
docker build -f Dockerfile.slim -t ml-slim .
```

## Run Inference
### Single image

```bash
docker run --rm ml-fat python inference.py example.jpg
docker run --rm ml-slim python inference.py example.jpg
```

### Multiple images from test_images/ folder

If you want to run inference on multiple images, mount the local folder inside the container:
```bash
docker run --rm -v $(pwd)/test_images:/app/test_images ml-fat python inference.py
docker run --rm -v $(pwd)/test_images:/app/test_images ml-slim python inference.py
```

The script will print top-3 predicted classes for each image.
