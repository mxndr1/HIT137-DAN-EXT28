"""
Simplified adapters around Hugging Face pipelines.

- BaseAdapter (multiple inheritance): LoggingMixin + ValidationMixin
- GPT2TextAdapter: text-generation
- BLIPCaptionAdapter: image-to-text
"""
from typing import List, Dict, Any
from transformers import pipeline
from core.mixins import LoggingMixin, ValidationMixin
from core.decorators import timed, requires_input

class BaseAdapter(LoggingMixin, ValidationMixin):
    """Shares tiny helpers (logging + path checks)."""
    pass

class GPT2TextAdapter(BaseAdapter):
    """Very small wrapper around the GPT-2 text-generation pipeline."""
    def __init__(self, model_name: str = "openai-community/gpt2"):
        self.model_name = model_name
        self.pipe = None  # lazy init
        self.log("ready (lazy: pipeline will be built on first run)")

    def _ensure_loaded(self):
        if self.pipe is None:
            self.log("loading GPT-2 pipeline (first run may download weights)...")
            self.pipe = pipeline("text-generation", model=self.model_name)
            if getattr(self.pipe, "tokenizer", None) and self.pipe.tokenizer.pad_token_id is None:
                self.pipe.tokenizer.pad_token_id = self.pipe.tokenizer.eos_token_id
            self.log("pipeline loaded")

    @timed
    @requires_input
    def run(self, prompt: str, max_new_tokens: int = 60) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return self.pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            pad_token_id=self.pipe.tokenizer.eos_token_id,
        )

class BLIPCaptionAdapter(BaseAdapter):
    """Tiny wrapper around BLIP captioning pipeline."""
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        self.model_name = model_name
        self.pipe = None  # lazy init
        self.log("ready (lazy: pipeline will be built on first run)")

    def _ensure_loaded(self):
        if self.pipe is None:
            self.log("loading BLIP pipeline (first run may download weights)...")
            self.pipe = pipeline("image-to-text", model=self.model_name)
            self.log("pipeline loaded")

    @timed
    @requires_input
    def run(self, image_path: str, max_new_tokens: int = 30) -> List[Dict[str, Any]]:
        self.ensure_file_exists(image_path)
        self._ensure_loaded()
        return self.pipe(image_path, max_new_tokens=max_new_tokens)
