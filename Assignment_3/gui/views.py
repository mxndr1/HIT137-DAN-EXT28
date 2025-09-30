"""
Tkinter GUI (v2) for GPT-2 text generation and BLIP image captioning.
- Dark theme
- Clear prompt -> Generate Text (GPT-2)
- Clear Browse -> Generate Caption + Thumbnail (BLIP)
- Info overlay with model + OOP summary
- Top banner + bottom status bar so you can visually confirm v2 is running
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import inspect

from core.adapters import GPT2TextAdapter, BLIPCaptionAdapter

# ---- Colors ----
BG = "#1E1E1E"
FG = "#FFFFFF"
FIELD_BG = "#2A2A2A"
BTN_BG = "#2D2D2D"
BTN_HOVER = "#3C3C3C"
ACCENT = "#9ad4ff"   # for picked path
BANNER_BG = "#252525"
STATUS_BG = "#181818"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI — v2")  # <— version marker
        self.geometry("1000x720")
        self.configure(bg=BG)

        # state
        self.model_choice = tk.StringVar(value="Text Generation (GPT-2)")
        self.gpt2 = None
        self.blip = None
        self.image_path = None

        # ttk style
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TButton", background=BTN_BG, foreground=FG, padding=6)
        style.map("TButton",
                  background=[("active", BTN_HOVER), ("pressed", BTN_HOVER)],
                  foreground=[("active", FG), ("pressed", FG)])
        style.configure("TCombobox",
                        fieldbackground=FIELD_BG,
                        background=FIELD_BG,
                        foreground=FG)

        # build UI
        self._build_banner()
        self._build_main()
        self._build_info()
        self._build_statusbar()

        self._show_main()
        self._on_model_changed(self.model_choice.get())

    # ----------------- Top Banner (visual cue for v2) -----------------
    def _build_banner(self):
        banner = tk.Frame(self, bg=BANNER_BG, height=38)
        banner.pack(fill="x", side="top")
        tk.Label(
            banner,
            text="Tkinter AI GUI — v2  •  GPT-2 & BLIP",
            bg=BANNER_BG, fg=FG, anchor="w"
        ).pack(side="left", padx=12, pady=6)

        # Quick action: Info
        ttk.Button(banner, text="Model & OOP Info", command=self._show_info).pack(side="right", padx=10, pady=4)

    # ----------------- Build Main Screen -----------------
    def _build_main(self):
        self.main_frame = tk.Frame(self, bg=BG)

        # top bar
        top = tk.Frame(self.main_frame, bg=BG)
        top.pack(fill="x", padx=10, pady=8)

        tk.Label(top, text="Model:", fg=FG, bg=BG).pack(side="left")
        self.combo = ttk.Combobox(
            top,
            textvariable=self.model_choice,
            values=["Text Generation (GPT-2)", "Image Captioning (BLIP)"],
            state="readonly",
            width=32
        )
        self.combo.pack(side="left", padx=8)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._on_model_changed(self.model_choice.get()))

        # center content
        center = tk.Frame(self.main_frame, bg=BG)
        center.pack(fill="both", expand=True, padx=10, pady=8)

        # left: inputs
        self.input_frame = tk.Frame(center, bg=BG)
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # GPT-2 widgets
        self.prompt_label = tk.Label(self.input_frame, text="Enter your prompt:", fg=FG, bg=BG, anchor="w")
        self.prompt_text = tk.Text(self.input_frame, height=14, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG)
        self.btn_run_gpt2 = ttk.Button(self.input_frame, text="Generate Text", command=self._run_gpt2)
        self.btn_clear = ttk.Button(self.input_frame, text="Clear", command=lambda: self.prompt_text.delete("1.0", "end"))

        # BLIP widgets
        self.btn_browse = ttk.Button(self.input_frame, text="Browse Image", command=self._pick_image)
        self.btn_run_blip = ttk.Button(self.input_frame, text="Generate Caption", command=self._run_blip)
        self.lbl_image = tk.Label(self.input_frame, text="No image selected", fg="#BBBBBB", bg=BG)
        self.thumb_label = tk.Label(self.input_frame, bg=BG)
        self._thumb_img = None  # keep reference

        # right: output
        self.output = tk.Text(center, height=26, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG)
        self.output.grid(row=0, column=1, sticky="nsew")

        center.grid_columnconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)
        center.grid_rowconfigure(0, weight=1)

    # ----------------- Build Info Screen -----------------
    def _build_info(self):
        self.info_frame = tk.Frame(self, bg=BG)
        top = tk.Frame(self.info_frame, bg=BG)
        top.pack(fill="x", padx=10, pady=8)
        ttk.Button(top, text="← Back", command=self._show_main).pack(side="left", padx=6)
        tk.Label(top, text="Model Info & OOP Explanation", fg=FG, bg=BG).pack(side="left", padx=10)

        body = tk.Frame(self.info_frame, bg=BG)
        body.pack(fill="both", expand=True, padx=10, pady=8)

        self.model_info = tk.Text(body, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG)
        self.model_info.pack(side="left", fill="both", expand=True, padx=6)

        self.oop_info = tk.Text(body, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG)
        self.oop_info.pack(side="right", fill="both", expand=True, padx=6)

    # ----------------- Bottom Status Bar (visual cue for v2) -----------------
    def _build_statusbar(self):
        self.status = tk.StringVar(value="Ready.")
        bar = tk.Frame(self, bg=STATUS_BG, height=26)
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, textvariable=self.status, bg=STATUS_BG, fg="#BFBFBF", anchor="w").pack(side="left", padx=10)

    # ----------------- Navigation -----------------
    def _show_main(self):
        self.info_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def _show_info(self):
        self._fill_model_info()
        self._fill_oop_info()
        self.main_frame.pack_forget()
        self.info_frame.pack(fill="both", expand=True)

    # ----------------- Handlers -----------------
    def _on_model_changed(self, choice: str):
        # Clear input panel
        for w in self.input_frame.winfo_children():
            w.pack_forget()

        if "GPT-2" in choice:
            # GPT-2 inputs
            self.prompt_label.pack(anchor="w", pady=(0, 4))
            self.prompt_text.pack(fill="both", expand=True, padx=8, pady=6)
            bar = tk.Frame(self.input_frame, bg=BG)
            bar.pack(anchor="w", pady=2)
            self.btn_run_gpt2.pack(in_=bar, side="left", padx=(8, 6))
            self.btn_clear.pack(in_=bar, side="left")
            if self.gpt2 is None:
                self.gpt2 = GPT2TextAdapter()
                self._out("[Loaded] GPT-2 (first run may download model files)")
                self.status.set("GPT-2 ready.")
            else:
                self.status.set("GPT-2 selected.")
        else:
            # BLIP inputs
            self.btn_browse.pack(padx=8, pady=(4, 4), anchor="w")
            self.btn_run_blip.pack(padx=8, pady=(0, 4), anchor="w")
            self.lbl_image.pack(padx=8, anchor="w")
            self.thumb_label.pack(padx=8, pady=6, anchor="w")
            if self.blip is None:
                self.blip = BLIPCaptionAdapter()
                self._out("[Loaded] BLIP (first run may download model files)")
                self.status.set("BLIP ready.")
            else:
                self.status.set("BLIP selected.")

    def _pick_image(self):
        path = filedialog.askopenfilename(
            title="Choose image",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All files", "*.*")]
        )
        if path:
            self.image_path = path
            self.lbl_image.config(text=path, fg=ACCENT)
            self._out(f"[Picked] {path}")
            self.status.set("Image selected.")
            # thumbnail
            try:
                from PIL import Image, ImageTk
                img = Image.open(path)
                img.thumbnail((220, 220))
                self._thumb_img = ImageTk.PhotoImage(img)
                self.thumb_label.config(image=self._thumb_img, text="")
            except Exception as e:
                self.thumb_label.config(image="", text=f"(Could not load thumbnail: {e})", fg="#FF8888")

    def _run_gpt2(self):
        try:
            self.status.set("Generating with GPT-2...")
            prompt = self.prompt_text.get("1.0", "end").strip()
            outs = self.gpt2.run(prompt)
            for item in outs:
                self._out("GPT-2 → " + item.get("generated_text", "").strip())
            self.status.set("Done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self._out(f"[Error] {e}")
            self.status.set("Error.")

    def _run_blip(self):
        try:
            if not self.image_path:
                messagebox.showwarning("No image", "Please select an image first.")
                return
            self.status.set("Captioning with BLIP...")
            outs = self.blip.run(self.image_path)
            if isinstance(outs, dict):
                outs = [outs]
            for item in outs:
                self._out("BLIP → " + item.get("generated_text", "").strip())
            self.status.set("Done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self._out(f"[Error] {e}")
            self.status.set("Error.")

    # ----------------- Info Panel Fillers -----------------
    def _fill_model_info(self):
        choice = self.model_choice.get()
        if "GPT-2" in choice:
            txt = (
                "• Model: openai-community/gpt2\n"
                "• Task: text-generation\n"
                "• First run may download weights (cached)."
            )
        else:
            txt = (
                "• Model: Salesforce/blip-image-captioning-base\n"
                "• Task: image-to-text\n"
                "• First run may download weights (cached)."
            )
        self._set_text(self.model_info, txt)

    def _fill_oop_info(self):
        sig_t = str(inspect.signature(GPT2TextAdapter.run))
        sig_b = str(inspect.signature(BLIPCaptionAdapter.run))
        txt = (
            "• Encapsulation: Each adapter hides the HF pipeline and exposes run().\n"
            f"• Polymorphism: GPT2.run{sig_t} vs BLIP.run{sig_b}.\n"
            "• Multiple Inheritance: BaseAdapter = LoggingMixin + ValidationMixin.\n"
            "• Decorators: @requires_input checks input, @timed prints runtime."
        )
        self._set_text(self.oop_info, txt)

    # ----------------- Helpers -----------------
    def _out(self, line: str):
        self.output.insert("end", line + "\n")
        self.output.see("end")

    def _set_text(self, widget: tk.Text, content: str):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.config(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
