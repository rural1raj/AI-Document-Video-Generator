from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np


# ---------- LOAD FONTS ----------
def load_fonts(lang="en"):
    try:
        if lang == "hi":
            font_path = "fonts/hindi.ttf"   # Hindi font
        else:
            font_path = "arial.ttf"

        title_font = ImageFont.truetype(font_path, 60)
        heading_font = ImageFont.truetype(font_path, 40)
        text_font = ImageFont.truetype(font_path, 32)

    except:
        title_font = heading_font = text_font = ImageFont.load_default()

    return title_font, heading_font, text_font


# ---------- CENTER TEXT ----------
def draw_center(draw, text, y, font, color, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=color)


# ---------- PARSE TEXT ----------
def parse_lines(text):
    return [line.strip() for line in text.split("\n") if line.strip()]


# ---------- VIDEO CREATOR ----------
def create_video(text, audio_path, output_path, lang="en"):

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    width, height = 1280, 720

    title_font, heading_font, text_font = load_fonts(lang)

    lines = parse_lines(text)
    total_lines = len(lines)

    time_per_line = duration / max(total_lines, 1)

    # layout
    mask_top = 180
    mask_bottom = height - 40
    line_height = 40
    max_visible_lines = 10

    def make_frame(t):

        img = Image.new("RGB", (width, height), (10, 10, 35))
        draw = ImageDraw.Draw(img)

        # ===== MAIN TITLE (CENTER) =====
        draw_center(draw, "AI DESCRIPTION", 40, title_font, "cyan", width)

        # ===== SUB TITLE (CENTER) =====
        draw_center(draw, "DOCUMENT DESCRIPTION", 110, heading_font, "orange", width)

        # ===== MASK BOX =====
        draw.rectangle(
            [(40, mask_top), (width - 40, mask_bottom)],
            fill=(20, 20, 60)
        )

        # ===== CURRENT LINE INDEX =====
        current_index = int(t / time_per_line)
        current_index = min(current_index, total_lines - 1)

        # ===== SCROLL CONTROL =====
        start = max(0, current_index - max_visible_lines + 1)
        visible_lines = lines[start:current_index]

        y = mask_top + 20

        # ===== DRAW PREVIOUS LINES =====
        for line in visible_lines:
            if ":" in line:
                draw.text((60, y), line, font=heading_font, fill="orange")
            else:
                draw.text((60, y), line, font=text_font, fill="white")
            y += line_height

        # ===== CURRENT LINE TYPING =====
        current_line = lines[current_index]

        progress = (t % time_per_line) / time_per_line
        char_count = int(progress * len(current_line))
        typed_text = current_line[:char_count]

        draw.text((60, y), typed_text, font=text_font, fill="yellow")

        return np.array(img)

    # ===== FINAL VIDEO =====
    video = VideoClip(make_frame, duration=duration)
    video = video.set_audio(audio)

    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path