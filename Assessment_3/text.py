from transformers import pipeline
from ai_base import AIModel

class GPT2TextGen(AIModel):
    """Wrapper for GPT-2 text generation using Hugging Face pipeline."""

    name = "openai-community/gpt2"
    category = "Text Generation"

    def load(self):
        """Load the GPT-2 pipeline (only once)."""
        self._pipe = pipeline("text-generation", model=self.name)

    def run(self, prompt: str, max_new_tokens: int = 200) -> str:
        """Generate text continuation for a given prompt."""
        self.ensure_loaded()
        out = self._pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=0.95,
            temperature=0.9,
            eos_token_id=self._pipe.tokenizer.eos_token_id,
        )[0]["generated_text"]
        return out

# ---- Simple API for GUI ----
_singleton = None
def generate_text(prompt: str, max_new_tokens: int = 80) -> str:
    global _singleton
    if _singleton is None:
        _singleton = GPT2TextGen()
    return _singleton.run(prompt, max_new_tokens=max_new_tokens)

if __name__ == "__main__":
    print(generate_text("Charles Darwin University students are"))
