import os
import random
import pandas as pd
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import WhiteNoise, Sine

# Paths
excel_path = "E:\\Projects\\pytestvoiceinterface\\ePrescription_ScenarioFullAPI_TestMatrix.xlsx"
output_dir = "hospital_voices_merged"
os.makedirs(output_dir, exist_ok=True)

# Read Excel
df = pd.read_excel(excel_path)

# Language mapping
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Mixed (Eng+Beng)": "en",  # fallback
    "Mixed (Eng+Hin)": "en"
}

def generate_background_noise(duration_ms):
    """Simulate hospital/clinic environment noise"""
    noises = []

    # 1. Low background chatter = filtered white noise
    chatter = WhiteNoise().to_audio_segment(duration=duration_ms, volume=-45).low_pass_filter(500)
    noises.append(chatter)

    # 2. Typing clicks = short sine wave blips repeated
    typing = AudioSegment.silent(duration=duration_ms)
    for _ in range(random.randint(5, 12)):
        pos = random.randint(0, duration_ms - 200)
        click = Sine(1200).to_audio_segment(duration=50, volume=-30)
        typing = typing.overlay(click, position=pos)
    noises.append(typing)

    # 3. Footsteps = low thumps
    footsteps = AudioSegment.silent(duration=duration_ms)
    for _ in range(random.randint(3, 6)):
        pos = random.randint(0, duration_ms - 400)
        thump = Sine(80).to_audio_segment(duration=200, volume=-35).fade_in(50).fade_out(50)
        footsteps = footsteps.overlay(thump, position=pos)
    noises.append(footsteps)

    # 4. Ambient hum
    hum = Sine(60).to_audio_segment(duration=duration_ms, volume=-40)
    noises.append(hum)

    # Mix all noises
    bg_noise = AudioSegment.silent(duration=duration_ms)
    for n in noises:
        bg_noise = bg_noise.overlay(n)

    return bg_noise

def generate_with_effects(text, lang):
    # Convert text to audio
    tts = gTTS(text=text, lang=lang, slow=False)
    temp_file = "temp_tts.mp3"
    tts.save(temp_file)

    # Load TTS output
    voice = AudioSegment.from_file(temp_file, format="mp3")

    # Split into chunks at sentence boundaries (rough split at ".")
    parts = text.split(".")
    final_audio = AudioSegment.silent(duration=500)  # start with a small pause

    for part in parts:
        if not part.strip():
            continue
        # TTS for each chunk
        tts_chunk = gTTS(text=part.strip(), lang=lang, slow=False)
        chunk_file = "chunk.mp3"
        tts_chunk.save(chunk_file)
        chunk_audio = AudioSegment.from_file(chunk_file, format="mp3")

        # Add chunk + random pause (300–1500 ms)
        final_audio += chunk_audio
        final_audio += AudioSegment.silent(duration=random.randint(300, 1500))

    # Add simulated hospital/office background noise
    bg_noise = generate_background_noise(len(final_audio))
    final_audio = final_audio.overlay(bg_noise)

    # Clean up temp files
    if os.path.exists(temp_file): os.remove(temp_file)
    if os.path.exists("chunk.mp3"): os.remove("chunk.mp3")

    return final_audio

# Process each row
for idx, row in df.iterrows():
    case_id = row["Test Case ID"]
    lang = row["Language"]
    accent = row["Accent/Speech Style"]
    scenario = row["Scenario"]
    text = str(row["Sample Voice Input"])

    tts_lang = lang_map.get(lang, "en")

    # Generate audio with effects
    audio = generate_with_effects(text, tts_lang)

    # Save file
    safe_scenario = scenario.replace(" ", "_").replace("/", "-")
    file_name = f"{case_id}_{lang}_{accent}_{safe_scenario}.mp3"
    file_path = os.path.join(output_dir, file_name)
    audio.export(file_path, format="mp3")

    print(f"Generated: {file_name}")

print("All voices generated with realistic hospital/office background noise!")
