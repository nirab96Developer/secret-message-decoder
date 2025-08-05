# 🔐 Secret Message Decoder

**Caesar Cipher Decryption Tool with GUI**  
Python Final Project - The Secret Message from the Spy

---

## 📋 Project Information

**Student Name:** Nir Avitbul  
**Institution:** The College of Management  
**Course:** Introduction to Python (4372)  
**Project:** Final Project - "The Secret Message from the Spy"  
**Repository:** https://github.com/nirab96Developer/secret-message-decoder  
**Submission Date:** August 2025

---

## 🎯 Project Description

A comprehensive Python application that implements Caesar cipher encryption/decryption with automatic brute-force capabilities. The project features a modern GUI built with Tkinter, advanced text analysis using 10+ built-in Python functions, and interactive data visualization tools.

### ✨ Key Features

- 🔓 **Automatic Decryption** - Brute force algorithm to find the correct shift
- 📊 **Text Analysis** - Comprehensive analysis using 10+ Python built-in functions
- 📈 **Data Visualization** - Interactive graphs and charts using Tkinter Canvas
- 💾 **File Management** - Save/load encrypted and decrypted messages
- 📁 **JSON Export** - Export analysis results in JSON format
- 🔄 **Re-encryption** - Encrypt text with user-chosen shift
- 🎨 **Modern GUI** - User-friendly interface with multiple tabs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Tkinter (usually included with Python)
- No external libraries required

### Installation & Run

```bash
# Clone the repository
git clone https://github.com/nirab96Developer/secret-message-decoder.git
cd secret-message-decoder

# Run the application
python main.py



secret-message-decoder/
│
├── main.py # Entry point of the application
├── README.md # Project documentation (this file)
│
├── gui/
│ ├── **init**.py
│ └── interface.py # GUI implementation with Tkinter
│
├── modules/
│ ├── **init**.py
│ ├── cipher.py # Caesar cipher encryption/decryption logic
│ ├── text_analyzer.py # Text analysis with built-in functions
│ ├── file_handler.py # File I/O operations
│ └── visualizer.py # Graph and chart creation
│
├── data/
│ ├── encrypted_message.txt # Sample encrypted file
│ ├── decrypted/ # Folder for saved decrypted messages
│ └── operations.log # Operation history log
│
└── screenshots/ # Application screenshots

💻 Usage Guide
Step 1: Decrypting the Message

Load encrypted text:

Click "Load File" to load from file, or
Paste encrypted text directly into the text area

Auto Decrypt:

Click "Auto Decrypt" button
The program will try all 26 shifts automatically
Detect the correct shift by checking for common English words
Display the decrypted message and the detected shift value

Step 2: Text Analysis

Run Analysis:

After decryption, click "Analyze" button
Or navigate to the "Analysis" tab and click "Run Analysis"

View Results:

Total characters: 559
Total words: 95
Unique characters: 34
Unique words: 71
Longest word: "warehouse" (9 chars)
Shortest word: "a" (1 char)
Average word length: 4.1
Vowel percentage: 37.9%
Letter percentage: 73.6%
And more statistics...

Export Results:

Click "Export Report" to save analysis as JSON
File saved to: data/analysis_YYYYMMDD_HHMMSS.json

Step 3: Visualization and Interaction

Navigate to Visualizations tab
Select graph type:

Word Length - Distribution histogram
Character Types - Pie chart
Word Frequency - Bar chart
Shift Analysis - Line graph with best shift

Additional Features:

Save: Save decrypted text to file
Copy: Copy decrypted text to clipboard
Re-encrypt: Choose new shift (1-25) and encrypt again

🎯 Technical Implementation
Project Requirements Met ✅
According to the project instructions, all requirements have been successfully implemented:

1. Built-in Functions Used (10+ Required)
   FunctionUsage in ProjectLocationlen()Calculate lengths of strings and liststext_analyzer.pyset()Find unique characters and wordstext_analyzer.pymax()Find longest wordtext_analyzer.pymin()Find shortest wordtext_analyzer.pysum()Calculate totals and averagestext_analyzer.pysorted()Sort words by lengthtext_analyzer.pyany()Check if any word > 7 characterstext_analyzer.pyall()Check if all words are lowercasetext_analyzer.pyzip()Create word-length pairstext_analyzer.pymap()Apply functions to sequencestext_analyzer.pyfilter()Filter out empty stringstext_analyzer.pyenumerate()Create indexed word liststext_analyzer.pyCounterCount word frequenciestext_analyzer.py
2. Modular Code Structure ✅

Separate modules for different functionalities
Clean separation of GUI, logic, and data handling
Reusable functions throughout the codebase

3. Tkinter GUI Implementation ✅

Multi-tab interface for different features
ScrolledText widgets for input/output
Canvas for data visualization
File dialogs for loading/saving files
Message boxes for user feedback

4. Documentation ✅

Docstrings for all classes and functions
Inline comments explaining complex logic
README.md with comprehensive documentation
All code and comments in English

🔧 Algorithm Details
Caesar Cipher Encryption/Decryption
The Caesar cipher shifts each letter in the alphabet by a fixed number of positions:
pythondef encrypt_text(text: str, shift: int) -> str:
"""Encrypt text using Caesar cipher"""
shift = shift % 26 # Ensure shift is within 0-25
result = []

    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            encrypted_ch = chr((ord(ch) - base + shift) % 26 + base)
            result.append(encrypted_ch)
        else:
            result.append(ch)  # Keep non-alphabetic characters

    return ''.join(result)

Brute Force Decryption Algorithm
pythondef brute_force_decrypt(encrypted_text):
"""Try all 26 possible shifts"""
best_score = 0.0
best_shift = None
best_text = None

    for shift in range(26):
        decrypted = decrypt_text(encrypted_text, shift)
        score = calculate_word_score(decrypted)

        if score > best_score:
            best_score = score
            best_shift = shift
            best_text = decrypted

    return best_text, best_shift

Common English Words Detection
The program checks for these common English words to identify correct decryption:

"the", "and", "is", "message", "secret", "to", "of", "in", "for", "on", "with", "at", "by", "from", "this"

📊 Sample Data
Example Encrypted Message (Shift 13)
Guvf vf n frperg zrffntr sebz gur fcl. Gur zvffvba vf rkgerzryl vzcbegnag
naq zhfg or pbzcyrgrq orsber zvqavtug. Zrrg zr ng gur byq jnerubhfr arne gur qbpxf.
Oevat gur qbphzragf naq znxr fher lbh ner abg sbyybjrq. Gur cnffjbeq vf 'Oyhr Zbba'.
Gehfg ab bar rkprcg Ntrag Frira. Tbbq yhpx!
Decrypted Result
This is a secret message from the spy. The mission is extremely important
and must be completed before midnight. Meet me at the old warehouse near the docks.
Bring the documents and make sure you are not followed. The password is 'Blue Moon'.
Trust no one except Agent Seven. Good luck!

🐛 Troubleshooting
Common Issues and Solutions
IssueSolution"tkinter not found"Install tkinter: sudo apt-get install python3-tk (Linux) or reinstall Python with tkinter"Module not found"Ensure you're in the correct directory and all files are presentFile permission errorRun with appropriate permissions or as administratorGUI not displaying correctlyCheck display settings and tkinter version

🧪 Testing
The application includes a sample encrypted file that is automatically created on first run:

File: data/encrypted_message.txt
Shift: 13
Content: Secret spy message

Test Cases

Automatic Decryption Test

Load sample file
Click "Auto Decrypt"
Verify shift 13 is detected

Text Analysis Test

Run analysis on decrypted text
Verify all statistics are calculated

Visualization Test

Check all four graph types
Verify data is displayed correctly

File Operations Test

Save decrypted text
Export JSON report
Verify files are created

📝 License
This project is submitted as a final project for the Python programming course at The College of Management.
Educational use only.

👨‍💻 Author
Nir Avitbul
Student at The College of Management
Course: Introduction to Python (4372)
Email: nirabutbul41@gmail.com
GitHub: @nirab96Developer

🙏 Acknowledgments
Special thanks to the course instructor and The College of Management for the opportunity to work on this project.

© 2025 Nir Avitbul. All rights reserved.
```
