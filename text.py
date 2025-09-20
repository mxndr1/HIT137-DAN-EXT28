# text.py
from transformers import pipeline

# Load once, reuse (fast on subsequent calls)
_generator = pipeline(
    "text-generation",
    model="openai-community/gpt2",
    tokenizer="openai-community/gpt2",
)

def generate_text(prompt: str) -> str:
    """
    Generate a continuation for the prompt using GPT-2.
    Returns a single string.
    """
    out = _generator(
        prompt,
        max_new_tokens=80,     # adjust length
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
        eos_token_id=_generator.tokenizer.eos_token_id,
    )
    return out[0]["generated_text"]
