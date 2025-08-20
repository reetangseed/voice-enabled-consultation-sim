# set up Python 3.11 alongside Python 3.13 on your Windows system
# py -3.11 voicegeneratorwithnoise.py
# py -3.11 -m pip install gTTS pydub pandas openpyxl
import os
import random
import pandas as pd
from gtts import gTTS
from pydub import AudioSegment

excel_path = "E:\\Projects\\pytestvoiceinterface\\ePrescription_ScenarioFullAPI_TestMatrix.xlsx"
output_dir = "E:\\Projects\\pytestvoiceinterface\\generated_audio_realistic"
noise_dir = "E:\\Projects\\pytestvoiceinterface\\noise_samples"
interrupt_dir = "E:\\Projects\\pytestvoiceinterface\\interruptions"

os.makedirs(output_dir, exist_ok=True)

def add_background_noise(voice_file, output_file):
    """Mix background noise + interruptions with generated voice."""
    voice = AudioSegment.from_file(voice_file)

    # --- Background Noise ---
    noise_files = [f for f in os.listdir(noise_dir) if f.endswith((".mp3", ".wav"))]
    if noise_files:
        noise_file = os.path.join(noise_dir, random.choice(noise_files))
        noise = AudioSegment.from_file(noise_file)

        # Match duration
        if len(noise) < len(voice):
            noise = noise * (len(voice) // len(noise) + 1)
        noise = noise[:len(voice)]

        # Softer volume
        noise = noise - random.randint(20, 28)
        combined = voice.overlay(noise)
    else:
        combined = voice

    # --- Interruptions (20–30% chance) ---
    interrupt_files = [f for f in os.listdir(interrupt_dir) if f.endswith((".mp3", ".wav"))]
    if interrupt_files and random.random() < 0.3:  
        interrupt_file = os.path.join(interrupt_dir, random.choice(interrupt_files))
        interrupt = AudioSegment.from_file(interrupt_file)

        # Insert at a random timestamp
        insert_at = random.randint(2000, max(3000, len(combined) - 1000))
        combined = combined.overlay(interrupt - random.randint(5, 15), position=insert_at)

    # Normalize output
    combined = combined.normalize()
    combined.export(output_file, format="mp3")
    print(f"Saved: {output_file}")


df = pd.read_excel(excel_path)

for idx, row in df.iterrows():
    case_id = str(row["Test Case ID"])
    lang = row["Language"]
    accent = row["Accent/Speech Style"]
    scenario = row["Scenario"]
    text = str(row["Sample Voice Input"])

    # Map language to gTTS codes
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Mixed (Eng+Beng)": "en",  # fallback to English
        "Mixed (Eng+Hin)": "en"
    }
    tts_lang = lang_map.get(lang, "en")

    # Add slight pauses to simulate realism
    pause_variants = [".", "...", ",", " - ", ""]
    text_with_pauses = text + random.choice(pause_variants)

    # Generate audio
    tts = gTTS(text=text_with_pauses, lang=tts_lang, slow=False)

    # File naming convention
    safe_scenario = scenario.replace(" ", "_").replace("/", "-")
    file_name = f"{case_id}_{lang}_{accent}_{safe_scenario}.mp3"
    temp_file = os.path.join(output_dir, file_name.replace(".mp3", "_clean.mp3"))
    final_file = os.path.join(output_dir, file_name)

    tts.save(temp_file)
    add_background_noise(temp_file, final_file)
    os.remove(temp_file)

print("All scenario voice samples generated with pauses, noise, and interruptions!")
