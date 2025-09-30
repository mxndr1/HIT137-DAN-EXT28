'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG (VAN HOI DANG)- s395598
KEVIN ZHU (JIAWEI ZHU) - s387035
MEHRAAB FERDOUSE - s393148

'''

# Module: gui/views.py
# Project: Tkinter AI GUI
# Purpose:
#   - Build a dark-themed Tkinter app that runs two simple AI demos:
#     - GPT-2 text generation (prompt → completion)
#     - BLIP image captioning (image → caption)
#   - Keep the window responsive while models run in the background
#   - Show a busy overlay and spinner whenever work is in progress
#
# How this file is organised:
#   - Color constants
#   - App class (creates the window and all screens)
#   - Helpers for the busy overlay and threading
#   - Event handlers and model actions
#   - Small utilities (sentence trim, logging, set_text)
#
# Shortcuts:
#   - Ctrl+Enter: generate text
#   - Ctrl+Shift+C: clear the prompt
#
# First run:
#   - The first time each model runs, it may download files and then cache them

"""
Tkinter GUI (v2.6) for GPT-2 text generation and BLIP image captioning.
- Separate Status/Logs box
- GPT-2: Generate (replace) + Generate More (append)
- Output trimmed to the last '.', '!' or '?'
- Dark OptionMenu selector, thumbnail preview, banner, status bar
- Background thread with a busy overlay + spinner
- Shortcuts: Ctrl+Enter (Generate), Ctrl+Shift+C (Clear)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading            # runs long tasks off the main UI thread
import inspect              # shows readable method signatures in the OOP tab

from core.adapters import GPT2TextAdapter, BLIPCaptionAdapter  # adapters wrap the HF pipelines

# Colors and basic style
BG = "#1E1E1E"          # app background
FG = "#FFFFFF"          # main text color
FIELD_BG = "#2A2A2A"    # text field backgrounds
BTN_BG = "#2D2D2D"      # button normal color
BTN_HOVER = "#3C3C3C"   # button hover/active color
ACCENT = "#9ad4ff"      # highlight color (used for chosen path)
BANNER_BG = "#252525"   # banner background
STATUS_BG = "#181818"   # status bar background
OVERLAY_BG = "#000000"  # busy overlay background


class App(tk.Tk):
    """
    Main application window.
    - Create screens and widgets
    - Hold simple state (selected model, chosen image)
    - Run model work in the background and update the UI when it finishes
    """

    def __init__(self):
        """Set up the window, theme, widgets, shortcuts, and initial screen."""
        super().__init__()
        self.title("Tkinter AI GUI")        # set window title bar text
        self.geometry("1080x740")           # set a starting size that fits both columns well
        self.configure(bg=BG)               # apply dark background to root

        # Simple state
        self.model_choice = tk.StringVar(value="Text Generation (GPT-2)")  # drive the OptionMenu selection
        self.gpt2 = None     # hold GPT-2 adapter; load on first use to avoid slow start
        self.blip = None     # hold BLIP adapter; load on first use to avoid slow start
        self.image_path = None  # remember the last chosen image path for captioning

        # ttk button style (OptionMenu is a classic Tk widget, so we style it separately below)
        style = ttk.Style(self)             # create a ttk style object bound to this root
        try:
            style.theme_use("clam")         # pick a theme that supports more styling on Windows
        except Exception:
            pass                            # if theme is missing, safely continue with default
        style.configure("TButton", background=BTN_BG, foreground=FG, padding=6)  # apply button colors and padding
        style.map("TButton",
                  background=[("active", BTN_HOVER), ("pressed", BTN_HOVER)],   # change background on hover/press
                  foreground=[("active", FG), ("pressed", FG)])                 # keep text readable on hover/press

        # Build the main screens
        self._build_banner()     # create the top banner (title + info button)
        self._build_main()       # create the main interactive screen
        self._build_info()       # create the info screen (hidden at first)
        self._build_statusbar()  # create the bottom status bar

        # Handy shortcuts
        self.bind("<Control-Return>", lambda e: self._run_gpt2())       # run GPT-2 with Ctrl+Enter
        self.bind("<Control-Shift-C>", lambda e: self._clear_prompt())  # clear prompt with Ctrl+Shift+C

        # Busy overlay placeholders
        self._overlay = None     # later holds a full-window Frame during long tasks
        self._spinner = None     # later holds a ttk.Progressbar spinner in the overlay

        # Start on the main screen
        self._show_main()                                    # show the main interaction screen
        self._on_model_changed(self.model_choice.get())      # ensure the left panel matches the selected model

    # Banner (top strip)
    def _build_banner(self):
        """Create the top row with the title and the info button."""
        banner = tk.Frame(self, bg=BANNER_BG, height=38)     # make a fixed-height banner frame
        banner.pack(fill="x", side="top")                    # stretch horizontally at the top
        tk.Label(
            banner,
            text="Tkinter AI GUI  •  GPT-2 & BLIP",          # label text inside banner
            bg=BANNER_BG,
            fg=FG,
            anchor="w",                                      # align text to left inside label
        ).pack(side="left", padx=12, pady=6)                 # pack to left with some padding
        ttk.Button(
            banner,
            text="Model & OOP Info",
            command=self._show_info                          # clicking this swaps to info screen
        ).pack(side="right", padx=10, pady=4)

    # Main screen (inputs, logs, output)
    def _build_main(self):
        """Build the main interactive screen."""
        self.main_frame = tk.Frame(self, bg=BG)              # container for everything on the main screen

        # Model selector row
        top = tk.Frame(self.main_frame, bg=BG)               # row that holds the model selector
        top.pack(fill="x", padx=10, pady=8)                  # give it some breathing room

        tk.Label(top, text="Model:", fg=FG, bg=BG).pack(side="left", padx=(0, 6))  # label before the selector
        self.model_selector = tk.OptionMenu(
            top,
            self.model_choice,                                # variable that stores the selected value
            "Text Generation (GPT-2)",                        # first option
            "Image Captioning (BLIP)",                        # second option
            command=self._on_model_changed,                   # called whenever the selection changes
        )
        # Make the OptionMenu itself look dark (button area)
        self.model_selector.configure(
            bg=BTN_BG, fg=FG, activebackground=BTN_HOVER, activeforeground=FG, bd=1, highlightthickness=0
        )
        # Make the dropdown list look dark (menu area)
        self.model_selector["menu"].configure(
            bg=BTN_BG, fg=FG, activebackground=BTN_HOVER, activeforeground=FG
        )
        self.model_selector.pack(side="left")                # place the selector to the left

        # Two-column layout
        center = tk.Frame(self.main_frame, bg=BG)            # area that holds the input and output columns
        center.pack(fill="both", expand=True, padx=10, pady=8)  # expand so both sides grow with the window

        # Left column: inputs
        self.left_panel = tk.Frame(center, bg=BG)            # column for text prompt or image controls
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))  # use grid to share space cleanly

        # GPT-2 prompt widgets
        self.prompt_label = tk.Label(self.left_panel, text="Enter your prompt:", fg=FG, bg=BG, anchor="w")
        self.prompt_area = tk.Frame(self.left_panel, bg=BG)  # container for the prompt box and its buttons
        self.prompt_text = tk.Text(                          # multi-line prompt box
            self.prompt_area, height=14, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG  # white caret
        )
        self.btn_bar = tk.Frame(self.prompt_area, bg=BG)     # row holding GPT-2 buttons (always visible)
        self.btn_run_gpt2 = ttk.Button(self.btn_bar, text="Generate (Ctrl+Enter)", command=self._run_gpt2)
        self.btn_more_gpt2 = ttk.Button(self.btn_bar, text="Generate More ➕", command=self._run_gpt2_more)
        self.btn_clear = ttk.Button(self.btn_bar, text="Clear (Ctrl+Shift+C)", command=self._clear_prompt)

        # BLIP widgets
        self.blip_area = tk.Frame(self.left_panel, bg=BG)    # container for image picker and generate button
        self.btn_browse = ttk.Button(self.blip_area, text="Browse Image", command=self._pick_image)  # open file dialog
        self.btn_run_blip = ttk.Button(self.blip_area, text="Generate Caption", command=self._run_blip)
        self.lbl_image = tk.Label(self.blip_area, text="No image selected", fg="#BBBBBB", bg=BG)     # show path or hint
        self.thumb_label = tk.Label(self.blip_area, bg=BG)   # label where a small preview image appears
        self._thumb_img = None                                # keep a reference so the thumbnail stays visible

        # Right column: logs and output
        right = tk.Frame(center, bg=BG)                       # column for status logs and model output
        right.grid(row=0, column=1, sticky="nsew")            # share space with the left column

        tk.Label(right, text="Status / Logs", fg=FG, bg=BG, anchor="w").pack(fill="x", padx=2)  # logs title
        self.logs = tk.Text(                                  # text box to show small status lines
            right, height=6, wrap="word", bg=FIELD_BG, fg="#CFCFCF", insertbackground=FG
        )
        self.logs.pack(fill="x", padx=(0, 2), pady=(0, 6))    # make logs stretch horizontally

        tk.Label(right, text="Output", fg=FG, bg=BG, anchor="w").pack(fill="x", padx=2)          # output title
        self.output = tk.Text(                                 # text box for model results
            right, height=22, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG
        )
        self.output.pack(fill="both", expand=True, padx=(0, 2))  # allow it to grow in both directions

        # Make both columns stretch nicely as the window resizes
        center.grid_columnconfigure(0, weight=1)              # left column grows
        center.grid_columnconfigure(1, weight=1)              # right column grows
        center.grid_rowconfigure(0, weight=1)                 # row grows vertically

    # Info screen (full-page view)
    def _build_info(self):
        """Build the screen that shows model info and a short OOP explanation."""
        self.info_frame = tk.Frame(self, bg=BG)               # separate frame for the info screen

        top = tk.Frame(self.info_frame, bg=BG)                # header row with a back button
        top.pack(fill="x", padx=10, pady=8)
        ttk.Button(top, text="← Back", command=self._show_main).pack(side="left", padx=6)  # return to main screen
        tk.Label(top, text="Model Info & OOP Explanation", fg=FG, bg=BG).pack(side="left", padx=10)

        body = tk.Frame(self.info_frame, bg=BG)               # body with two side-by-side text panes
        body.pack(fill="both", expand=True, padx=10, pady=8)

        self.model_info = tk.Text(                            # left text pane shows model details
            body, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG
        )
        self.model_info.pack(side="left", fill="both", expand=True, padx=6)

        self.oop_info = tk.Text(                              # right text pane shows OOP notes
            body, wrap="word", bg=FIELD_BG, fg=FG, insertbackground=FG
        )
        self.oop_info.pack(side="right", fill="both", expand=True, padx=6)

    # Status bar (bottom strip)
    def _build_statusbar(self):
        """Create the bottom status bar for short updates like 'Ready' or 'Done'."""
        self.status = tk.StringVar(value="Ready.")            # store short messages for the user
        bar = tk.Frame(self, bg=STATUS_BG, height=26)         # small strip at the bottom
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, textvariable=self.status, bg=STATUS_BG, fg="#BFBFBF", anchor="w")\
            .pack(side="left", padx=10)

    # Simple navigation between the two screens
    def _show_main(self):
        """Show the main screen."""
        self.info_frame.pack_forget()                         # hide the info screen if it is visible
        self.main_frame.pack(fill="both", expand=True)        # show the main screen

    def _show_info(self):
        """Show the info screen with fresh text."""
        self._fill_model_info()                               # write fresh model info
        self._fill_oop_info()                                 # write fresh OOP info
        self.main_frame.pack_forget()                         # hide the main screen
        self.info_frame.pack(fill="both", expand=True)        # show the info screen

    # Busy overlay helpers
    def _set_controls_state(self, state: str):
        """
        Enable or disable interactive widgets.
        - This prevents double-clicks while the app is working.
        """
        controls = [
            self.model_selector,                               # the OptionMenu button at the top
            getattr(self, "btn_run_gpt2", None),               # GPT-2 generate button
            getattr(self, "btn_more_gpt2", None),              # GPT-2 generate more button
            getattr(self, "btn_clear", None),                  # clear prompt button
            getattr(self, "btn_browse", None),                 # BLIP browse button
            getattr(self, "btn_run_blip", None),               # BLIP generate caption button
        ]
        for c in controls:
            if c is None:
                continue                                       # skip any that are not currently on screen
            try:
                c.config(state=state)                          # set state to "disabled" or "normal"
            except Exception:
                pass                                           # ignore styling issues on some platforms

    def _show_busy(self, message: str = "Working..."):
        """
        Show a full-window overlay with a spinner and a short message.
        - This clearly shows that a task is running.
        """
        if self._overlay is not None:
            return                                             # ignore if the overlay is already present
        self._set_controls_state("disabled")                   # block buttons while busy

        self._overlay = tk.Frame(self, bg=OVERLAY_BG)          # full-screen frame
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)  # cover the window

        inner = tk.Frame(self._overlay, bg=BANNER_BG, padx=18, pady=16)  # small card in the middle
        inner.place(relx=0.5, rely=0.5, anchor="center")       # center the card

        tk.Label(inner, text=message, bg=BANNER_BG, fg=FG).pack(pady=(0, 10))  # show the message
        self._spinner = ttk.Progressbar(inner, mode="indeterminate", length=260)  # show the spinner
        self._spinner.pack()
        self._spinner.start(12)                                # start spinner animation

    def _hide_busy(self):
        """Remove the overlay and re-enable the controls."""
        try:
            if self._spinner is not None:
                self._spinner.stop()                           # stop spinner if it exists
        except Exception:
            pass
        self._spinner = None
        if self._overlay is not None:
            self._overlay.destroy()                            # destroy the overlay frame
        self._overlay = None
        self._set_controls_state("normal")                     # re-enable buttons

    def _run_async(self, work_fn, on_success, on_error, message: str = "Working..."):
        """
        Run a function on a background thread and update the UI when it finishes.
        - work_fn returns a result
        - on_success(result) runs on the main thread
        - on_error(error) runs on the main thread
        """
        self._show_busy(message)                               # show busy overlay before starting

        def worker():
            try:
                result = work_fn()                             # run the task off the UI thread
                # use after(0, ...) so callbacks run safely in the UI thread
                self.after(0, lambda: (on_success(result), self._hide_busy()))
            except Exception as e:
                self.after(0, lambda: (on_error(e), self._hide_busy()))

        threading.Thread(target=worker, daemon=True).start()   # daemon thread ends when app closes

    # Event handlers and layout switching
    def _on_model_changed(self, choice: str):
        """Switch the left panel inputs based on the selected model."""
        # Remove any previous widgets in the left panel
        for w in self.left_panel.winfo_children():
            w.pack_forget()                                    # hide and remove layout

        if "GPT-2" in choice:
            # Show the prompt area and buttons
            self.prompt_label.pack(anchor="w", pady=(0, 4))    # show label above the prompt
            self.prompt_area.pack(fill="both", expand=True)    # make the area expand with the window
            self.prompt_text.pack(fill="both", expand=True, padx=8, pady=(6, 0))  # grow the text box
            self.btn_bar.pack(fill="x", side="bottom", pady=6) # keep buttons visible at bottom
            self.btn_run_gpt2.pack(side="left", padx=(8, 6))   # place the main generate button
            self.btn_more_gpt2.pack(side="left", padx=(0, 6))  # place the generate-more button
            self.btn_clear.pack(side="left")                   # place the clear button

            if self.gpt2 is None:
                self.gpt2 = GPT2TextAdapter()                  # load adapter only once when first needed
                self._log("[Loaded] GPT-2 (first run may download model files)")
                self.status.set("GPT-2 ready.")
            else:
                self.status.set("GPT-2 selected.")
        else:
            # Show image controls
            self.blip_area.pack(fill="x", anchor="w")          # show the image control row
            self.btn_browse.pack(padx=8, pady=(4, 4), anchor="w")   # place the file picker button
            self.btn_run_blip.pack(padx=8, pady=(0, 4), anchor="w") # place the caption button
            self.lbl_image.pack(padx=8, anchor="w")                 # show the current path or hint
            self.thumb_label.pack(padx=8, pady=6, anchor="w")       # show the preview (if any)

            if self.blip is None:
                self.blip = BLIPCaptionAdapter()               # load adapter only once when first needed
                self._log("[Loaded] BLIP (first run may download model files)")
                self.status.set("BLIP ready.")
            else:
                self.status.set("BLIP selected.")

    def _pick_image(self):
        """Open a file picker, remember the path, and show a small thumbnail."""
        path = filedialog.askopenfilename(                     # open a native file dialog
            title="Choose image",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All files", "*.*")],
        )
        if path:
            self.image_path = path                             # remember the chosen image path
            self.lbl_image.config(text=path, fg=ACCENT)        # show it on screen in accent color
            self._log(f"[Picked] {path}")                      # also write into the logs panel
            self.status.set("Image selected.")
            # Try to load a small preview using Pillow
            try:
                from PIL import Image, ImageTk                 # import here so Pillow is only needed if used
                img = Image.open(path)                         # open selected image
                img.thumbnail((220, 220))                      # resize in-place to fit a small box
                self._thumb_img = ImageTk.PhotoImage(img)      # convert to Tk image and keep a reference
                self.thumb_label.config(image=self._thumb_img, text="")  # show the preview
            except Exception as e:
                # if preview fails (unsupported format, missing Pillow, etc.), show a short note
                self.thumb_label.config(image="", text=f"(Could not load thumbnail: {e})", fg="#FF8888")

    # Model actions: GPT-2
    def _run_gpt2(self):
        """Generate new text from the prompt and replace the Output box."""
        prompt = self.prompt_text.get("1.0", "end").strip()   # read everything from the prompt, trim spaces

        def work():
            return self.gpt2.run(prompt)                      # ask the adapter to generate text

        def ok(outs):
            text = outs[0].get("generated_text", "").strip()  # take the first result and trim
            text = self._trim_to_sentence(text)               # cut to the last full sentence
            self._set_text(self.output, text)                 # show result in read-only style
            self.status.set("Done.")                          # update status bar

        def err(e):
            messagebox.showerror("Error", str(e))             # show a dialog with the error message
            self._log(f"[Error] {e}")                         # also write to logs
            self.status.set("Error.")                         # update status bar

        self.status.set("Generating with GPT-2...")           # show a short status
        self._run_async(work, ok, err, message="Generating text with GPT-2…")  # run it on a worker thread

    def _run_gpt2_more(self):
        """Continue the current output and append more text."""
        # If Output is empty, fall back to the prompt text as the seed
        current = self.output.get("1.0", "end").strip() or self.prompt_text.get("1.0", "end").strip()

        def work():
            return self.gpt2.run(current)                     # ask the adapter to continue from current text

        def ok(outs):
            new_text = outs[0].get("generated_text", "").strip()  # full text that includes old content
            # If the new text repeats the old text at the start, only take the extra part
            suffix = new_text[len(current):] if new_text.startswith(current) else new_text
            suffix = self._trim_to_sentence(suffix)           # trim suffix to the last full sentence

            self.output.config(state="normal")                # enable the widget temporarily
            self.output.insert("end", suffix)                 # append the new part
            self.output.see("end")                            # scroll to the bottom
            self.output.config(state="disabled")              # lock it again
            self.status.set("Done.")

        def err(e):
            messagebox.showerror("Error", str(e))
            self._log(f"[Error] {e}")
            self.status.set("Error.")

        self.status.set("Generating more with GPT-2...")
        self._run_async(work, ok, err, message="Adding more text…")

    def _clear_prompt(self):
        """Clear the GPT-2 prompt box."""
        self.prompt_text.delete("1.0", "end")                 # delete from first char to end of text
        self.status.set("Prompt cleared.")                    # update status bar so the user sees a confirmation

    # Model actions: BLIP
    def _run_blip(self):
        """Generate a caption for the selected image and show it in Output."""
        if not self.image_path:                                # stop if the user has not chosen an image yet
            messagebox.showwarning("No image", "Please select an image first.")
            return

        def work():
            return self.blip.run(self.image_path)              # ask the adapter to caption the image

        def ok(outs):
            if isinstance(outs, dict):                         # normalise to a list if adapter returns a dict
                outs = [outs]
            # join all captions with a line break (usually there is just one)
            text = "\n".join(item.get("generated_text", "").strip() for item in outs)
            self._set_text(self.output, text)                  # show caption in read-only style
            self.status.set("Done.")

        def err(e):
            messagebox.showerror("Error", str(e))
            self._log(f"[Error] {e}")
            self.status.set("Error.")

        self.status.set("Captioning with BLIP...")
        self._run_async(work, ok, err, message="Generating caption with BLIP…")

    # Info text fillers (populate the info screen on demand)
    def _fill_model_info(self):
        """Write a short description for the selected model."""
        choice = self.model_choice.get()                       # read current selection from the OptionMenu
        if "GPT-2" in choice:
            txt = (
                "Model: openai-community/gpt2\n"
                "Task: text generation. Enter a prompt on the left and click Generate. "
                "The first run may download model weights and cache them locally."
            )
        else:
            txt = (
                "Model: Salesforce/blip-image-captioning-base\n"
                "Task: image captioning. Choose an image, then click Generate Caption. "
                "The first run may download weights and cache them."
            )
        self._set_text(self.model_info, txt)                   # write into the left info pane

    def _fill_oop_info(self):
        """Write a short, friendly explanation of the OOP ideas in this project."""
        sig_t = str(inspect.signature(GPT2TextAdapter.run))    # show method signature for clarity
        sig_b = str(inspect.signature(BLIPCaptionAdapter.run))
        txt = (
            "Encapsulation: Each adapter hides the Hugging Face pipeline and exposes a simple run() method. "
            f"For example, GPT2TextAdapter.run{sig_t} accepts text, while BLIPCaptionAdapter.run{sig_b} accepts an image path.\n\n"
            "Polymorphism: The GUI calls run() on the active adapter without caring which model it is. "
            "Both adapters implement run(), but they handle different inputs and outputs.\n\n"
            "Multiple Inheritance: BaseAdapter mixes in LoggingMixin and ValidationMixin so adapters automatically get "
            "basic logging and file checks without repeating code.\n\n"
            "Decorators: @requires_input prevents empty prompts or missing paths, and @timed prints how long the model call took. "
            "These are applied around run() so the core logic stays clean."
        )
        self._set_text(self.oop_info, txt)                     # write into the right info pane

    # Small helpers
    def _trim_to_sentence(self, text: str) -> str:
        """
        Keep text up to the last full sentence.
        - A sentence ends with '.', '!' or '?'
        - If none are present, return the trimmed text as-is
        """
        last = max(text.rfind("."), text.rfind("!"), text.rfind("?"))  # find the last sentence end
        if last != -1:
            return text[: last + 1]                         # include the punctuation mark
        return text.strip()                                  # fall back to whitespace-trimmed text

    def _log(self, line: str):
        """Append a single line to the Status/Logs box and scroll to the end."""
        self.logs.insert("end", line + "\n")                  # add the line and a newline
        self.logs.see("end")                                  # keep the latest line visible

    def _set_text(self, widget: tk.Text, content: str):
        """
        Replace the contents of a tk.Text widget while keeping it read-only for the user.
        - Temporarily enable the widget to edit it, then disable it again
        """
        widget.config(state="normal")                         # allow editing from code
        widget.delete("1.0", "end")                           # clear old text
        widget.insert("1.0", content)                         # write new text
        widget.config(state="disabled")                       # lock it for the user


# Standard Tk entry-point pattern
if __name__ == "__main__":
    app = App()                                               # create the app instance
    app.mainloop()                                            # start the Tk event loop
