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
5. [Technologies Used](#technologies-used)
6. [How to Run the Scripts](#how-to-run-the-scripts)

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
│   │   └── temperatures/ (multiple CSV files for each year)
│   │
│   ├── Q3/
│   │   ├── HIT137_DANEXT28_A2_Q3.py
│   │   └── assets/
│   │       ├── image1.jpg
│   │       └── image2.jpg
│   │
│   └── HIT137 Assignment 2 S1 2025.pdf
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

This Python program analyzes temperature data collected from multiple weather stations in Australia. The data is stored in multiple CSV files under a `temperatures` folder, with each file representing one year's data. The program processes all CSV files and performs the following analyses:

* **Seasonal Average:** Calculates the average temperature for each Australian season (Summer: Dec-Feb, Autumn: Mar-May, Winter: Jun-Aug, Spring: Sep-Nov) across all stations and all years. Results are saved to `average_temp.txt`.

  * Output example: `Summer: 28.5°C`

* **Temperature Range:** Identifies the station(s) with the largest temperature range (difference between the highest and lowest temperature ever recorded at that station). Results are saved to `largest_temp_range_station.txt`.

  * Output example: `Station ABC: Range 45.2°C (Max: 48.3°C, Min: 3.1°C)`
  * Multiple stations are listed if tied.

* **Temperature Stability:** Determines the station(s) with the most stable temperatures (smallest standard deviation) and the most variable temperatures (largest standard deviation). Results are saved to `temperature_stability_stations.txt`.

  * Output example:

    * `Most Stable: Station XYZ: StdDev 2.3°C`
    * `Most Variable: Station DEF: StdDev 12.8°C`
  * Multiple stations are listed if tied.

### Question 3: Recursive Turtle Pattern

This Python program uses a recursive function with the `turtle` graphics library to generate intricate geometric patterns. The pattern generation follows these rules:

* Start with a regular polygon.
* For each edge of the polygon:

  1. Divide the edge into three equal segments.
  2. Replace the middle segment with two sides of an equilateral triangle pointing inward (creating an indentation).
  3. This transforms one straight edge into four smaller edges, each 1/3 the length of the original edge.
  4. Recursively apply the same process to each of the four new edges up to a specified depth, creating increasingly complex designs.

## Technologies Used

* **Python 3.x**
* **os**, **pandas**, **sys** (for file handling and data processing)
* **turtle** (for recursive pattern generation)

## How to Run the Scripts

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mxndr1/HIT137-DAN-EXT28.git
   cd HIT137-DAN-EXT28
   ```

2. **Install Required Libraries**

   Ensure you have Python 3.x installed. Then, install the necessary libraries using pip:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: If a `requirements.txt` file is not provided, manually install the required libraries using pip.*

3. **Run the Scripts**

   Navigate to the respective assignment folder and run the desired script:

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

   Follow the on-screen prompts or instructions in the terminal.
