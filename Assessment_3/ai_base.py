# ai_base.py
from abc import ABC, abstractmethod

class AIModel(ABC):
    name: str = ""
    category: str = ""

    def __init__(self):
        self._loaded = False
        self._pipe = None

    @abstractmethod
    def load(self): ...
    @abstractmethod
    def run(self, user_input): ...

    def ensure_loaded(self):
        if not self._loaded:
            self.load()
            self._loaded = True
