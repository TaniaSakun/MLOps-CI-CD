import torch
from torchvision import models

# Load pretrained model (mobilenet_v2)
model = models.mobilenet_v2(pretrained=True)
model.eval()

# Convert to TorchScript
example_input = torch.rand(1, 3, 224, 224)
traced_script_module = torch.jit.trace(model, example_input)

# Save
traced_script_module.save("model.pt")
print("Saved model.pt")
