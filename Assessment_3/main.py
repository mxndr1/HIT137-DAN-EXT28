import tkinter as tk
from gui_app import App          # <-- change to your GUI file name
import image, text               # the two files above

if __name__ == "__main__":
    app = App()        # no root argument
    # app.set_providers(caption_fn=..., text_fn=...)  # if you’re wiring models here
    app.mainloop()

    # Attach providers (these are exactly the signatures your GUI expects)
    #app.set_providers(
        #caption_fn=image.generate_caption,   # (image_path: str) -> str
        #text_fn=text.generate_text          # (prompt: str) -> str
    #)

    
