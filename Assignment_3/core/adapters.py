"""
Simplified adapters around Hugging Face pipelines.

- BaseAdapter uses multiple inheritance to pull in two small helpers:
  - LoggingMixin: prints simple messages to the log
  - ValidationMixin: checks things like file paths
- GPT2TextAdapter wraps a text-generation pipeline (GPT-2)
- BLIPCaptionAdapter wraps an image-to-text pipeline (BLIP)
"""

from typing import List, Dict, Any
from transformers import pipeline
from core.mixins import LoggingMixin, ValidationMixin
from core.decorators import timed, requires_input


class BaseAdapter(LoggingMixin, ValidationMixin):
    """
    Share tiny helpers across all adapters.
    - LoggingMixin adds a .log(message) method
    - ValidationMixin adds small checks like ensure_file_exists(path)
    """
    pass


class GPT2TextAdapter(BaseAdapter):
    """Wrap a GPT-2 text-generation pipeline in a small, easy interface."""

    def __init__(self, model_name: str = "openai-community/gpt2"):
        # remember which model to load
        self.model_name = model_name
        # keep the pipeline empty until the first run (lazy load)
        self.pipe = None
        # show a small note in logs so we know the adapter is constructed
        self.log("ready (lazy: pipeline builds on first run)")

    def _ensure_loaded(self):
        """
        Build the HF pipeline the first time it is needed.
        - This avoids slow app startup
        - It also triggers a model download the first time on a new machine
        """
        if self.pipe is None:
            self.log("loading GPT-2 pipeline (first run may download weights)...")
            # create a standard text-generation pipeline
            self.pipe = pipeline("text-generation", model=self.model_name)
            # make sure the tokenizer has a pad token id
            # some GPT-2 tokenizers do not set this by default
            if getattr(self.pipe, "tokenizer", None) and self.pipe.tokenizer.pad_token_id is None:
                self.pipe.tokenizer.pad_token_id = self.pipe.tokenizer.eos_token_id
            self.log("pipeline loaded")

    @timed                     # measure how long the generation takes
    @requires_input            # prevent calling run("") with an empty prompt
    def run(self, prompt: str, max_new_tokens: int = 60) -> List[Dict[str, Any]]:
        """
        Generate text from a prompt and return the raw HF output list.
        - prompt: user text that starts the generation
        - max_new_tokens: how many new tokens the model adds
        """
        self._ensure_loaded()  # make sure the pipeline exists
        # call the pipeline with common sampling settings
        return self.pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,                 # enable sampling so outputs vary
            temperature=0.9,                # control randomness (higher = more random)
            top_p=0.95,                     # nucleus sampling cutoff
            pad_token_id=self.pipe.tokenizer.eos_token_id,  # keep padding safe for GPT-2
        )


class BLIPCaptionAdapter(BaseAdapter):
    """Wrap a BLIP image captioning pipeline in a small, easy interface."""

    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        # remember which model to load
        self.model_name = model_name
        # keep the pipeline empty until the first run (lazy load)
        self.pipe = None
        self.log("ready (lazy: pipeline builds on first run)")

    def _ensure_loaded(self):
        """
        Build the HF pipeline the first time it is needed.
        - This may download weights on a new device
        """
        if self.pipe is None:
            self.log("loading BLIP pipeline (first run may download weights)...")
            # create a standard image-to-text (captioning) pipeline
            self.pipe = pipeline("image-to-text", model=self.model_name)
            self.log("pipeline loaded")

    @timed                       # measure how long captioning takes
    @requires_input              # prevent calling run(None) or run("") 
    def run(self, image_path: str, max_new_tokens: int = 30) -> List[Dict[str, Any]]:
        """
        Caption an image file and return the raw HF output list.
        - image_path: path to an image on disk
        - max_new_tokens: limit the length of the caption
        """
        # make sure the file path is valid before running the model
        self.ensure_file_exists(image_path)
        self._ensure_loaded()     # make sure the pipeline exists
        # call the pipeline; it returns a list of dicts with 'generated_text'
        return self.pipe(image_path, max_new_tokens=max_new_tokens)
