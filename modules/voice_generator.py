from gtts import gTTS
import os
import time
import re


# ---------- CLEAN + FORMAT FOR VOICE ----------
def prepare_text_for_voice(text, lang="en"):

    if not text or not text.strip():
        return "No content available"

    # remove unwanted symbols
    text = re.sub(r'[*\-•]', '', text)

    # convert headings to natural speech
    replacements_en = {
        "TITLE:": "Title.",
        "SUMMARY:": "Summary.",
        "SKILLS:": "Skills include.",
        "EXPERIENCE:": "Experience includes.",
        "PROJECTS:": "Projects are.",
        "EDUCATION:": "Education details."
    }

    replacements_hi = {
        "TITLE:": "शीर्षक.",
        "SUMMARY:": "सारांश.",
        "SKILLS:": "कौशल हैं.",
        "EXPERIENCE:": "अनुभव में शामिल है.",
        "PROJECTS:": "परियोजनाएं हैं.",
        "EDUCATION:": "शिक्षा विवरण."
    }

    replacements = replacements_hi if lang == "hi" else replacements_en

    for key, val in replacements.items():
        text = text.replace(key, val)

    # clean lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # join with pause
    final_text = ". ".join(lines)

    return final_text


# ---------- GENERATE VOICE ----------
def generate_voice(text, output_folder, lang="en"):

    # ✅ ensure folder is valid (NOT file)
    if output_folder.endswith(".mp3"):
        raise Exception("Output folder गलत है (file path दे दिया है)")

    # ✅ create folder safely
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        raise Exception(f"Folder create failed: {str(e)}")

    # ✅ unique filename (avoid overwrite + permission issue)
    filename = f"voice_{int(time.time())}.mp3"
    output_path = os.path.join(output_folder, filename)

    # ✅ prepare text
    voice_text = prepare_text_for_voice(text, lang)

    # ✅ gTTS limit safe (split long text)
    chunks = []
    max_len = 2500

    while len(voice_text) > max_len:
        split_index = voice_text.rfind(".", 0, max_len)
        if split_index == -1:
            split_index = max_len
        chunks.append(voice_text[:split_index])
        voice_text = voice_text[split_index:]

    chunks.append(voice_text)

    # ✅ generate voice
    try:
        temp_files = []

        for i, chunk in enumerate(chunks):
            temp_file = os.path.join(output_folder, f"temp_{i}.mp3")

            tts = gTTS(text=chunk, lang=("hi" if lang == "hi" else "en"))
            tts.save(temp_file)

            temp_files.append(temp_file)

        # merge audio files
        with open(output_path, "wb") as outfile:
            for tf in temp_files:
                with open(tf, "rb") as infile:
                    outfile.write(infile.read())

        # delete temp files
        for tf in temp_files:
            try:
                os.remove(tf)
            except:
                pass

    except Exception as e:
        raise Exception(f"Voice generation failed: {str(e)}")

    return output_path