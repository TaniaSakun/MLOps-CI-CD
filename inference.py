import torch
from torchvision import transforms
from PIL import Image
import os
import json

# Load TorchScript model
model = torch.jit.load("model.pt")
model.eval()

# Preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# Load ImageNet class names
with open("imagenet_classes.txt") as f:
    categories = [line.strip() for line in f.readlines()]

# Folder with test images
TEST_DIR = "test_images"
images = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if f.endswith((".jpg", ".jpeg",".png"))]

# Run inference for all images
for img_path in images:
    image = Image.open(img_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        top3_prob, top3_catid = torch.topk(output, 3)

    result = {categories[catid]: float(prob) for prob, catid in zip(top3_prob[0], top3_catid[0])}
    print(f"Results for {img_path}:")
    print(json.dumps(result, indent=2))
