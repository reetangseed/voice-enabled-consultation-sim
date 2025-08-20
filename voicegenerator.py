#  pip install gtts pandas openpyxl - run this dependency in terminal
import pandas as pd
from gtts import gTTS
import os

# Path to your test matrix Excel
excel_path = "E:\\Projects\\pytestvoiceinterface\\ePrescription_ScenarioFullAPI_TestMatrix.xlsx"
output_dir = "voice_test_data_big_scenario"

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Load Excel
df = pd.read_excel(excel_path)

# Loop through each test case
for idx, row in df.iterrows():
    case_id = row["Test Case ID"]
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

    # Generate audio
    tts = gTTS(text=text, lang=tts_lang, slow=False)

    # File naming convention
    safe_scenario = scenario.replace(" ", "_").replace("/", "-")
    file_name = f"{case_id}_{lang}_{accent}_{safe_scenario}.mp3"
    file_path = os.path.join(output_dir, file_name)

    try:
        tts.save(file_path)
        print(f"Saved: {file_name}")
    except Exception as e:
        print(f"⚠️ Failed for {case_id}: {e}")
