import tkinter as tk
from tkinter import ttk, scrolledtext
from models import ModelManager
from oop_explanation import OOPExplanation


# Base class: Generic GUI
class BaseGUI:
    def __init__(self, title="Tkinter Al GUl", size="700x500"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)

    def run(self):
        self.root.mainloop()

# Subclass: actual GUI Implementation (method overriding)
class MyApp(BaseGUI):
    def __init__(self):
        super().__init__()
        self.model_manager = ModelManager()
        self.create_widgets()

    def create_widgets(self):
        # Dropdown menu for model selection
        self.model_var = tk.StringVar()
        ttk.Label(self.root, text='Select Model:').pack(pady=5)
        self.model_dropdown = ttk.Combobox(
            self.root, textvariable=self.model_var,
            values=list(self.model_manager.models.keys())
        )
        self.model_dropdown.current(0)
        self.model_dropdown.pack()

        # Input field
        ttk.Label(self.root, text='Input Data:').pack(pady=5)
        self.input_entry = ttk.Entry(self.root, width=50)
        self.input_entry.pack()

        # Output area
        ttk.Label(self.root, text='Output Result:').pack(pady=5)
        self.output_area = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.output_area.pack()

        # Buttons
        ttk.Button(self.root, text='Run Model', command=self.run_model).pack(pady=5)
        ttk.Button(self.root, text='Show OOP Explanation', command=self.show_oop_explanation).pack(pady=5)

    def run_model(self):
        model_name = self.model_var.get()
        text_input = self.input_entry.get()

        # Run model and show result
        result = self.model_manager.run(model_name, text_input)
        self.output_area.insert(tk.END, f"\nModel:{model_name}\nResult:{result}\n")

    def show_oop_explanation(self):
        explanation = OOPExplanation().get_explanation()
        self.output_area.insert(tk.END, f"\n{explanation}\n")