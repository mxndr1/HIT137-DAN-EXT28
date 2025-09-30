<p align="center">
  <strong>CDU acknowledges the traditional custodians of the lands on which we live, learn, work, and play. We pay our respects to the Larrakia people, the traditional custodians of this land</strong>
</p>

# HIT137: Software Now, Group: DAN-EXT28

This repository contains the solutions to the HIT137 unit assignments completed by Group DANEXT28 at Charles Darwin University (CDU) for Semester 1, 2025.

## Table of Contents

1. [Group Members](#group-members)  
2. [Repository Structure](#repository-structure)  
3. [Assignment 1 Overview](#assignment-1-overview)  
   * [Question 1a: Triangle Checker](#question-1a-triangle-checker)  
   * [Question 1b: Square Creator](#question-1b-square-creator)  
   * [Question 2 and 3: Collaborative Programming Document](#question-2-and-3-collaborative-programming-document)  
4. [Assignment 2 Overview](#assignment-2-overview)  
   * [Question 1: Encryption Program](#question-1-encryption-program)  
   * [Question 2: Temperature Data Analysis](#question-2-temperature-data-analysis)  
   * [Question 3: Recursive Turtle Pattern](#question-3-recursive-turtle-pattern)  
5. [Assignment 3 Overview](#assignment-3-overview)  
6. [Technologies Used](#technologies-used)  
7. [How to Run the Scripts](#how-to-run-the-scripts)

## Group Members

* **Fateen Ishraq Rahman** (Student ID: s387983)  
* **Hendrick Dang (Van Hoi Dang)** (Student ID: s395598)  
* **Kevin Zhu (Jiawei Zhu)** (Student ID: 387035)  
* **Mehraab Ferdouse** (Student ID: s393148)

## Repository Structure

```
HIT137-DAN-EXT28/
│
├── Assignment_1/
│   ├── HIT137_DANEXT28_Q1a.py
│   ├── HIT137_DANEXT28_Q1b.py
│   └── HIT137_DANEXT28_Q2_and_Q3.docx
│
├── Assignment_2/
│   ├── Q1/
│   │   ├── HIT137_DANEXT28_A2_Q1.py
│   │   └── raw_text.txt
│   │
│   ├── Q2/
│   │   ├── HIT137_DANEXT28_A2_Q2.py
│   │   └── temperatures (multiple CSV files for each year)
│   │
│   ├── Q3/
│   │   └── HIT137_DANEXT28_A2_Q3.py
│   │
│   └── HIT137 Assignment 2 S1 2025.pdf
│
├── Assignment_3/
│   ├── app_main.py
│   ├── core/
│   │   ├── adapters.py
│   │   ├── decorators.py
│   │   └── mixins.py
│   ├── gui/
│   │   └── views.py
│   ├── docs/
│   │   ├── model_info.md
│   │   └── oop_explained.md
│   ├── requirements.txt
│   └── HIT137 Assignment 3 S1 2025.pdf
│
└── README.md
```

## Assignment 1 Overview

### Question 1a: Triangle Checker
* Python program that takes three integer inputs.  
* Determines whether the three integers can form a triangle.

### Question 1b: Square Creator
* Python program that takes a single integer input.  
* Creates a square in the command line.  
  * Outline made of `*` symbols.  
  * Middle area filled with spaces.  
  * Square size determined by the input integer.

### Question 2 and 3: Collaborative Programming Document
* Word document containing:  
  * Screenshot proof of all four group members communicating via Microsoft Teams.  
  * An essay discussing collaborative programming practices.

## Assignment 2 Overview

### Question 1: Encryption Program
This Python script implements a Caesar cipher encryption algorithm. It reads a plaintext file (`raw_text.txt`), encrypts its contents using a specified shift value, and writes the encrypted text to `encrypted_text.txt`. The script also provides a decryption function to revert the encrypted text back to its original form and a verification function that verifies whether the decrypted file is identical to the original raw text.

### Question 2: Temperature Data Analysis
This Python program analyzes temperature data collected from multiple weather stations in Australia. The program processes multiple CSV files and performs analyses such as:  
* **Seasonal Average** across all years and stations.  
* **Temperature Range** (largest max-min difference).  
* **Temperature Stability** (most stable and most variable stations).  

Results are saved to output text files (e.g., `average_temp.txt`, `largest_temp_range_station.txt`).

### Question 3: Recursive Turtle Pattern
This Python program uses a recursive function with the `turtle` graphics library to generate geometric patterns. It transforms polygon edges into smaller recursive shapes, creating increasingly complex designs.

## Assignment 3 Overview

The task is to design a **Tkinter GUI** that demonstrates object-oriented programming concepts and integrates Hugging Face AI models.

### Requirements
* The GUI must show clear examples of:
  * Multiple inheritance  
  * Multiple decorators  
  * Encapsulation  
  * Polymorphism  
  * Method overriding  
* The GUI integrates **two free Hugging Face models** from different categories:
  * **GPT-2 (Text Generation)** – generates text based on user prompts.  
  * **BLIP (Image Captioning)** – generates captions for uploaded images.  
* Users can select input type (text or image) from a drop-down menu, run it through the models, and view results.  
* The GUI contains:  
  * A section for explaining OOP concepts and where they appear in the code.  
  * A section for showing information about the chosen models.  
  * Standard navigation widgets (buttons, drop-downs, etc.).  


* The code is split into multiple files (`app_main.py`, `core/`, `gui/`, etc.) rather than being in one file.  


### Key Learning
* How to design and structure a Python GUI application.  
* Applying OOP principles in a practical coding project.  
* Working with external AI libraries and models (Hugging Face).  
* Collaborative coding and version control with GitHub.

## Technologies Used
* **Python 3.x**  
* **pandas**, **os**, **sys** (for data processing and file handling)  
* **turtle** (for recursive graphics)  
* **tkinter** (for GUI development)  
* **transformers** (Hugging Face library for GPT-2 and BLIP integration)

## How to Run the Scripts

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mxndr1/HIT137-DAN-EXT28.git
   cd HIT137-DAN-EXT28
   ```

2. **Install Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Programs**
   * For Assignment 1:
     ```bash
     python Assignment_1/HIT137_DANEXT28_Q1a.py
     python Assignment_1/HIT137_DANEXT28_Q1b.py
     ```
   * For Assignment 2:
     ```bash
     python Assignment_2/Q1/HIT137_DANEXT28_A2_Q1.py
     python Assignment_2/Q2/HIT137_DANEXT28_A2_Q2.py
     python Assignment_2/Q3/HIT137_DANEXT28_A2_Q3.py
     ```
   * For Assignment 3:
     ```bash
     python Assignment_3/app_main.py
     ```

   Follow the on-screen prompts or instructions in the GUI/terminal.
