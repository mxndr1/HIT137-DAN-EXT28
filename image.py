# image.py
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load once, reuse
_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Optional: move to GPU if available
_device = "cuda" if torch.cuda.is_available() else "cpu"
_model.to(_device)

def generate_caption(image_path: str) -> str:
    """
    Generate a caption for the image at image_path using BLIP.
    Returns a single string.
    """
    img = Image.open(image_path).convert("RGB")
    inputs = _processor(images=img, return_tensors="pt").to(_device)

    with torch.no_grad():
        # Short, clean captions; increase max_new_tokens if you want longer
        ids = _model.generate(**inputs, max_new_tokens=30)
    caption = _processor.decode(ids[0], skip_special_tokens=True)
    return caption.strip()
