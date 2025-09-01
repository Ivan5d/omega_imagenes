import os
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

# Model setup (load once)
model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
torch.set_float32_matmul_precision(['high', 'highest'][0])
model.to('cuda')
model.eval()

# Data settings
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def remove_background(input_image_path):
    """
    Removes the background from the input image and returns the result as a PIL Image.
    Args:
        input_image_path (str): Path to the input image.
    Returns:
        PIL.Image: The image with background removed (with alpha channel).
    """
    try:
        image = Image.open(input_image_path).convert('RGB')
        
        # Preprocess the image
        input_images = transform_image(image).unsqueeze(0).to('cuda')

        # Prediction
        with torch.no_grad():
            preds = model(input_images)[-1].sigmoid().cpu()
        
        # Post-processing
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)
        image.putalpha(mask)

        return image

    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")
        return None

