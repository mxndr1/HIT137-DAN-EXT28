# image.py
from transformers import pipeline
from PIL import Image
from ai_base import AIModel

class BLIPCaption(AIModel):
    """Wrapper for BLIP image captioning (image -> text)."""

    name = "Salesforce/blip-image-captioning-base"
    category = "Image-to-Text"

    def load(self):
        """Load the BLIP pipeline once."""
        self._pipe = pipeline("image-to-text", model=self.name)

    def run(self, image_path: str) -> str:
        """Return a caption for the given image path."""
        self.ensure_loaded()
        img = Image.open(image_path).convert("RGB")
        caption = self._pipe(img)[0]["generated_text"]
        return caption

# ---- Simple API for GUI ----
_singleton = None
def caption_image(image_path: str) -> str:
    global _singleton
    if _singleton is None:
        _singleton = BLIPCaption()
    return _singleton.run(image_path)

if __name__ == "__main__":
    # Change this to a real image path on your machine before running:
    print(caption_image(r"C:\Users\Admin\Pictures\sample.jpg"))
