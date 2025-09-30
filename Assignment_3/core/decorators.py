'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG (VAN HOI DANG)- s395598
KEVIN ZHU (JIAWEI ZHU) - s387035
MEHRAAB FERDOUSE - s393148

'''

"""
Very small, easy-to-read decorators.

- timed: measures how long a function takes and prints it
- requires_input: makes sure the first argument is not empty
"""

import time
from functools import wraps


def timed(fn):
    """
    Decorator that times how long a function runs.
    - Prints the duration in seconds to the console
    - Useful for seeing if model calls are slow
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        start = time.time()          # remember the start time
        out = fn(*args, **kwargs)    # run the actual function
        dur = time.time() - start    # measure how long it took
        print(f"[timed] {fn.__qualname__} took {dur:.2f}s")
        return out                   # give back the original result
    return inner


def requires_input(fn):
    """
    Decorator that checks the first argument passed to a function.
    - If it is None or an empty string, it raises an error
    - Prevents running a model with no prompt or no file path
    """
    @wraps(fn)
    def inner(self, first_arg, *args, **kwargs):
        # stop early if the input is missing
        if first_arg is None:
            raise ValueError("Input is required.")
        # stop if the input is a string but contains no characters
        if isinstance(first_arg, str) and not first_arg.strip():
            raise ValueError("Input is required (empty string).")
        # otherwise, continue with the normal function
        return fn(self, first_arg, *args, **kwargs)
    return inner
