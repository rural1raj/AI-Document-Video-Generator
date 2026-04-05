import google.generativeai as genai
from config import GEMINI_API_KEY
import re
import time

# ---------- CONFIG ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


# ---------- CLEAN TEXT ----------
def clean_input_text(text):
    if not text:
        return ""

    # remove unwanted symbols
    text = re.sub(r'[^\w\s.,:]', ' ', text)

    # normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ---------- FINAL FORMAT CLEANER ----------
def clean_output_text(text):
    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # remove unwanted bullets or symbols
        line = re.sub(r'[*•\-]+', '', line)

        # avoid broken words
        line = line.replace(" ,", ",").replace(" .", ".")

        lines.append(line)

    return "\n".join(lines)


# ---------- MAIN PROCESSOR ----------
def process_text(text, lang="en"):

    text = clean_input_text(text)

    language = "Hindi" if lang == "hi" else "English"

    prompt = f"""
    You are an expert AI content formatter and video script generator.

    Convert the given document into a highly professional, clean, and structured format.

    Language: {language}

    IMPORTANT RULES:

    1. Structure must be:
    TITLE:
    SUMMARY:
    SKILLS:
    EXPERIENCE:
    PROJECTS:
    EDUCATION:

    2. Write short, clear lines (video friendly)
    3. Each line must be complete (no word cutting)
    4. Avoid long paragraphs
    5. No bullet symbols, no special characters
    6. Use simple professional words
    7. Make content engaging for video narration
    8. Do not repeat content
    9. Keep headings exactly as defined
    10. Content must look clean in slide and video

    OUTPUT FORMAT EXAMPLE:

    TITLE:
    Software Engineer

    SUMMARY:
    Experienced developer with strong problem solving skills
    Skilled in building scalable applications

    SKILLS:
    Python programming
    Web development
    API integration

    EXPERIENCE:
    Worked on real world projects
    Built scalable systems

    PROJECTS:
    Developed automation tools
    Created AI based solutions

    EDUCATION:
    Bachelor degree in Computer Science

    Now process this document:
    """

    try:
        response = model.generate_content(prompt + text)

        if not response.text:
            return text

        output = response.text

    except Exception:
        time.sleep(3)
        return text[:2000]

    # clean final output
    output = clean_output_text(output)

    return output