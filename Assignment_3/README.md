# Tkinter AI GUI (Simple)

## Run
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app_main.py
```

> First run may download model weights (GPT-2 + BLIP). They are cached for future runs.
> Offline hint: copy `~/.cache/huggingface/` from a machine that has the models.


## Screenshot
![Main View](docs/screenshot.png)

- Left panel switches between **GPT-2 prompt** and **BLIP image controls**.
- When you pick an image, a **thumbnail preview** appears under the file path.
- Right panel shows outputs and status messages (e.g., first-run downloads).
