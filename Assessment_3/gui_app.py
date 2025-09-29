"""
Tkinter AI GUI (OOP showcase)
- Demonstrates: multiple inheritance, encapsulation, polymorphism & overriding,
  and multiple decorators (@dataclass, @abstractmethod, @property, @classmethod,
  and a custom @threaded).
- Stays model-agnostic: concrete model classes override a common interface.
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Dict, Type, Tuple, Any, Callable
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


# ------------------------ Decorators ---------------------------------
def threaded(fn: Callable):
    """
    Run a bound method in a worker thread. If the method returns
    (header:str, text:str, status:str), we safely update the UI
    on the main thread via .after(0, ...).
    """
    def wrapper(self, *args, **kwargs):
        def run():
            try:
                result = fn(self, *args, **kwargs)
                if isinstance(result, tuple) and len(result) == 3:
                    header, text, status = result
                    self.after(0, lambda: (self._append_output(header, text),
                                           self._set_status(status)))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
        threading.Thread(target=run, daemon=True).start()
    return wrapper

# ------------------------ Model layer --------------------------------

@dataclass(frozen=True)
class ModelMeta:
    name: str
    category: str   # "Text" or "Vision" etc.
    description: str

class BaseModel(ABC):
    """Abstract base for all models (polymorphism target)."""
    meta: ModelMeta

    @abstractmethod
    def run(self, input_value: str) -> str:
        """Do the model's main work and return a result."""
        ...

class CaptionModel(BaseModel):
    """Intermediate type so the GUI can type-check capabilities."""
    def run(self, image_path: str) -> str:  # override signature semantics
        # child classes must implement real logic
        return super().run(image_path)  # pragma: no cover

class TextModel(BaseModel):
    """Intermediate type so the GUI can type-check capabilities."""
    def run(self, prompt: str) -> str:
        return super().run(prompt)  # pragma: no cover

# ---- Concrete implementations (override 'run') ----------------------

class BlipCaptionModel(CaptionModel):
    meta = ModelMeta(
        name="BLIP — Bootstrapping Language-Image Pretraining",
        category="Vision",
        description="Generates natural language captions from images."
    )

    # class-level lazy cache (so we load once, reuse)
    _processor: BlipProcessor | None = None
    _model: BlipForConditionalGeneration | None = None
    _device: str = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    def _ensure_loaded(cls):
        if cls._processor is None or cls._model is None:
            cls._processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            cls._model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            ).to(cls._device)

    def run(self, image_path: str) -> str:  # overriding
        self.__class__._ensure_loaded()
        img = Image.open(image_path).convert("RGB")
        inputs = self._processor(images=img, return_tensors="pt").to(self._device)
        with torch.no_grad():
            ids = self._model.generate(**inputs, max_new_tokens=30)
        caption = self._processor.decode(ids[0], skip_special_tokens=True)
        return caption.strip()


class Gpt2TextModel(TextModel):
    meta = ModelMeta(
        name="GPT-2 — Generative Pretrained Transformer 2",
        category="Text",
        description="Continues a prompt with fluent, plausible text."
    )

    _pipe = None  # class-level cache

    @classmethod
    def _get_pipe(cls):
        if cls._pipe is None:
            cls._pipe = pipeline(
                "text-generation",
                model="openai-community/gpt2",
                tokenizer="openai-community/gpt2",
            )
        return cls._pipe

    def run(self, prompt: str) -> str:  # overriding
        pipe = self.__class__._get_pipe()
        out = pipe(
            prompt,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            eos_token_id=pipe.tokenizer.eos_token_id,
        )[0]["generated_text"]

        # If you prefer only the continuation (not the echoed prompt), use:
        # return out[len(prompt):].lstrip()
        return out







#class BlipCaptionModel(CaptionModel):
#    meta = ModelMeta(
#        name="BLIP — Bootstrapping Language-Image Pretraining",
#        category="Vision",
#        description="Generates natural language captions from images."
#    )
#
#    def run(self, image_path: str) -> str:  # overriding
#        # TODO: replace placeholder with real BLIP inference
#        return f"[BLIP demo caption for] {image_path}"

#class Gpt2TextModel(TextModel):
#    meta = ModelMeta(
#        name="GPT-2 — Generative Pretrained Transformer 2",
#        category="Text",
#        description="Continues a prompt with fluent, plausible text."
#    )

#    def run(self, prompt: str) -> str:  # overriding
#        # TODO: replace placeholder with real GPT-2 inference
#        return f"[GPT-2 demo text for] {prompt}"

# ---- Registry (factory) ---------------------------------------------

class ModelRegistry:
    _registry: Dict[str, Type[BaseModel]] = {
        "BLIP (Image Captioning)": BlipCaptionModel,
        "GPT-2 (Text Generation)": Gpt2TextModel,
    }

    @classmethod
    def keys(cls):
        return list(cls._registry.keys())

    @classmethod
    def create(cls, key: str) -> BaseModel:
        return cls._registry[key]()  # raises KeyError if missing


# ---------------------- GUI mixins (multiple inheritance) ------------

class StatusBarMixin:
    def _build_statusbar(self):
        self._status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self._status_var,
                  relief="sunken", anchor="w", padding=4)\
            .grid(row=2, column=0, columnspan=2, sticky="ew")

    def _set_status(self, msg: str):
        self._status_var.set(msg)

class ProviderMixin:
    """
    Encapsulates model attachment & selection.
    - Uses @property for selected_model (encapsulation).
    - The GUI talks to BaseModel polymorphically (no concrete imports in GUI).
    """
    _selected_model_key: Optional[str] = None
    _selected_model: Optional[BaseModel] = None

    @property
    def selected_model_key(self) -> Optional[str]:
        return self._selected_model_key

    @selected_model_key.setter
    def selected_model_key(self, key: str):
        self._selected_model_key = key
        self._selected_model = ModelRegistry.create(key)  # new concrete instance
        self._update_model_info()
        # Optional: flip input mode based on category
        if self._selected_model.meta.category.lower() == "vision":
            self._input_mode.set("image")
        else:
            self._input_mode.set("text")

    def has_caption(self) -> bool:
        return isinstance(self._selected_model, CaptionModel)

    def has_textgen(self) -> bool:
        return isinstance(self._selected_model, TextModel)


# ---------------------- Main App (multiple inheritance) --------------

class App(tk.Tk, StatusBarMixin, ProviderMixin):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI — OOP concepts")
        self.geometry("1000x620")

        # root grid: Left wider than right
        self.columnconfigure(0, weight=5, minsize=600)  # left
        self.columnconfigure(1, weight=3, minsize=360)  # right
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        # encapsulated state
        self._image_path: Optional[str] = None
        self._input_mode = tk.StringVar(value="text")

        self._build_menu()
        self._build_left()
        self._build_right()
        self._build_statusbar()

        # default model
        self._model_combo.set("GPT-2 (Text Generation)")
        self.selected_model_key = "GPT-2 (Text Generation)"

    # -------------- UI build ----------------------------------------
    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Image", command=self._on_browse_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        help_menu = tk.Menu(menubar, tearoff=0) 
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Tkinter AI GUI — OOP demo")) 
        menubar.add_cascade(label="Help", menu=help_menu)

    def _build_left(self):
        left = ttk.LabelFrame(self, text="User Input", padding=8)
        left.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(6, weight=1)  # info panel expands

        # model selection
        row = ttk.Frame(left); row.grid(row=0, column=0, sticky="ew")
        row.columnconfigure(1, weight=1)
        ttk.Label(row, text="Model Selection:").grid(row=0, column=0, sticky="w", padx=(0,6))
        self._model_combo = ttk.Combobox(row, state="readonly", values=ModelRegistry.keys())
        self._model_combo.grid(row=0, column=1, sticky="ew")
        self._model_combo.bind("<<ComboboxSelected>>",
                               lambda e: setattr(self, "selected_model_key", self._model_combo.get()))

        # input mode radios
        r = ttk.Frame(left); r.grid(row=1, column=0, sticky="w", pady=(6,0))
        ttk.Radiobutton(r, text="Text", variable=self._input_mode, value="text").pack(side="left", padx=4)
        ttk.Radiobutton(r, text="Image", variable=self._input_mode, value="image").pack(side="left", padx=4)

        # browse + prompt
        ttk.Button(left, text="Browse Image", command=self._on_browse_image)\
            .grid(row=2, column=0, sticky="ew", pady=(6,2))
        ttk.Label(left, text="Prompt for Text Model:")\
            .grid(row=3, column=0, sticky="w", pady=(8,2))
        self._prompt = ttk.Entry(left); self._prompt.grid(row=4, column=0, sticky="ew")

        # actions
        actions = ttk.Frame(left); actions.grid(row=5, column=0, sticky="ew", pady=8)
        actions.columnconfigure((0,1,2), weight=1)
        ttk.Button(actions, text="Caption",  command=self._action_caption).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(actions, text="Generate", command=self._action_generate).grid(row=0, column=1, sticky="ew", padx=2)
    

        # info panel
        info = ttk.LabelFrame(left, text="Model Information & Explanation", padding=8)
        info.grid(row=6, column=0, sticky="nsew", pady=(6,0))
        info.columnconfigure(0, weight=1, minsize=320, uniform="info")
        info.columnconfigure(1, weight=1, minsize=320, uniform="info")
        info.rowconfigure(0, weight=1)

        self._info_left = ttk.LabelFrame(info, text="Selected Model Info:")
        self._info_left.grid(row=0, column=0, sticky="nsew", padx=(0,6))
        self._info_left.columnconfigure(0, weight=1)
        self._model_info = tk.Text(self._info_left, height=12, wrap="word"); self._model_info.grid(row=0, column=0, sticky="nsew")

        self._info_right = ttk.LabelFrame(info, text="OOP Concepts Explanation:")
        self._info_right.grid(row=0, column=1, sticky="nsew", padx=(6,0))
        self._info_right.columnconfigure(0, weight=1)
        self._oop_info = tk.Text(self._info_right, height=12, wrap="word"); self._oop_info.grid(row=0, column=0, sticky="nsew")
        self._seed_oop_text()

    def _build_right(self):
        right = ttk.LabelFrame(self, text="Output", padding=8)
        right.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        right.columnconfigure(0, weight=1); right.rowconfigure(0, weight=1)
        self._output = tk.Text(right, wrap="word")
        self._output.grid(row=0, column=0, sticky="nsew")

    # -------------- Info helpers ------------------------------------
    def _update_model_info(self):
        m = self._selected_model.meta if self._selected_model else None
        self._model_info.configure(state="normal"); self._model_info.delete("1.0", "end")
        if m:
            self._model_info.insert("end", f"• Model Name: {m.name}\n")
            self._model_info.insert("end", f"• Category: {m.category}\n")
            self._model_info.insert("end", f"• Description: {m.description}\n")
        else:
            self._model_info.insert("end", "Select a model to view details.")
        self._model_info.configure(state="disabled")

    def _seed_oop_text(self):
        self._oop_info.configure(state="normal"); self._oop_info.delete("1.0", "end")
        self._oop_info.insert("end",
            "• Multiple Inheritance: App inherits from tk.Tk, StatusBarMixin, ProviderMixin\n"
            "• Encapsulation: state & helpers kept inside App; property-selected model\n"
            "• Polymorphism & Overriding: BaseModel.run overridden by Blip/GPT-2; GUI calls BaseModel uniformly\n"
            "• Decorators: @dataclass, @abstractmethod, @property, @classmethod, custom @threaded\n"
        )
        self._oop_info.configure(state="disabled")

    # -------------- Actions (threaded) --------------------------------
    def _on_browse_image(self):
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")])
        if path:
            self._image_path = path
            self._set_status(f"Loaded: {path}")

    @threaded
    def _action_caption(self) -> Tuple[str, str, str]:
        if not self.has_caption():
            raise RuntimeError("Selected model is not an image captioner.")
        if not self._image_path:
            raise RuntimeError("Load an image first.")
        self._set_status("Captioning…")
        out = self._selected_model.run(self._image_path)
        return ("Caption", out, "Caption done")

    @threaded
    def _action_generate(self) -> Tuple[str, str, str]:
        if not self.has_textgen():
            raise RuntimeError("Selected model is not a text generator.")
        prompt = self._prompt.get().strip()
        if not prompt:
            raise RuntimeError("Type a prompt first.")
        self._set_status("Generating…")
        out = self._selected_model.run(prompt)
        return ("Text", out, "Text done")

    

    # -------------- UI utils -----------------------------------------
    def _append_output(self, header: str, text: str):
        self._output.insert("end", f"\n[{header}]\n{text}\n")
        self._output.see("end")


# ---------------------- entry point ----------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()


