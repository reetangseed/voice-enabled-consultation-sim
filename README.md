# Voice-Enabled Prescription Test Data Generator

This project provides a **Python-based voice generator** that creates realistic audio samples for testing **e-prescription interfaces**.  
It supports **English, Hindi, and Bengali** with options for different accents, natural pauses, and background noise simulation.

## 📌 Features
- Generate **voice samples from Excel test scenarios**  
- Supports **English, Hindi, Bengali, and mixed language input**  
- Adds **realistic pauses** and **background noise** (clinic, typing, chatter, etc.)  
- Helps QA teams **test voice-to-text transcription accuracy** in real-world conditions  
- Customizable file naming for easy organization

## 🗂 Project Structure
```
your-repo/
│── scenarios.xlsx               # Input test scenarios (with Test Case ID, Language, Accent, etc.)
│── voicegeneratorwithnoise.py   # Main script to generate audio samples
│── requirements.txt             # Dependencies
│── README.md                    # Project documentation
│── output/                      # Generated audio files
```

## ⚙️ Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/voice-enabled-prescription-generator.git
   cd voice-enabled-prescription-generator
   ```

2. Install dependencies: mention in the python files (check comments)

3. Install **FFmpeg** (required for `pydub`):
   - Windows:  
     Download from [FFmpeg.org](https://ffmpeg.org/download.html) and add it to PATH  
   - Mac (Homebrew):  
     ```bash
     brew install ffmpeg
     ```  
   - Linux:  
     ```bash
     sudo apt-get install ffmpeg
     ```

## ▶️ Usage
1. Prepare your **Excel file** (`scenarios.xlsx`) with columns:
   - `Test Case ID`  
   - `Language`  
   - `Accent/Speech Style`  
   - `Scenario`  
   - `Sample Voice Input`

2. Run the script:
   ```bash
   python voicegeneratorwithnoise.py
   ```

3. Generated audio will be saved in the `output/` folder with filenames like:
   ```
   TC01_English_Indian_DoctorConsultation.mp3
   ```

## 🎧 Example Use Cases
- Testing **doctor dictation accuracy** in e-prescription systems  
- Validating **multilingual transcription** (English/Hindi/Bengali)  
- Simulating **real clinic environments** with background noise  
- Training/testing **AI speech recognition models**  

## 📌 Requirements
- Python 3.8+  
- `gTTS`, `pydub`, `openpyxl`  

## 👩‍💻 Contributing
Feel free to fork this repo, add more **languages, noise types, or scenario templates**, and open a pull request!

---

💡 *Built for QA teams to test voice-enabled medical consultation systems.*  
