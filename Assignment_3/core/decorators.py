"""
Very small, easy-to-read decorators.
"""
import time
from functools import wraps

def timed(fn):
    """Print how long the wrapped function took (seconds)."""
    @wraps(fn)
    def inner(*args, **kwargs):
        start = time.time()
        out = fn(*args, **kwargs)
        dur = time.time() - start
        print(f"[timed] {fn.__qualname__} took {dur:.2f}s")
        return out
    return inner

def requires_input(fn):
    """Ensure the first argument after `self` is non-empty (e.g., prompt or image path)."""
    @wraps(fn)
    def inner(self, first_arg, *args, **kwargs):
        if first_arg is None:
            raise ValueError("Input is required.")
        if isinstance(first_arg, str) and not first_arg.strip():
            raise ValueError("Input is required (empty string)."
)
        return fn(self, first_arg, *args, **kwargs)
    return inner
