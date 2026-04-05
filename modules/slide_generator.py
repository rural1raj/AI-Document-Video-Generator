from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


# ---------- LOAD FONTS ----------
def load_fonts():
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 70)
        heading_font = ImageFont.truetype("arialbd.ttf", 42)
        text_font = ImageFont.truetype("arial.ttf", 32)
    except:
        title_font = heading_font = text_font = ImageFont.load_default()

    return title_font, heading_font, text_font


# ---------- PARSE TEXT INTO SECTIONS ----------
def parse_sections(text):
    sections = []
    current_title = None
    current_content = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if ":" in line and line.split(":")[0].isupper():
            if current_title:
                sections.append((current_title, current_content))
            current_title = line
            current_content = []
        else:
            current_content.append(line)

    if current_title:
        sections.append((current_title, current_content))

    return sections


# ---------- CREATE SINGLE STRUCTURED SLIDE ----------
def create_single_slide(text, output_folder):

    width, height = 1920, 1080

    # background
    img = Image.new("RGB", (width, height), (8, 10, 35))
    draw = ImageDraw.Draw(img)

    title_font, heading_font, text_font = load_fonts()

    # ---------- MAIN TITLE ----------
    main_title = "AI GENERATED DESCRIPTION"
    draw.text((450, 40), main_title, font=title_font, fill="cyan")

    # ---------- SUB TITLE ----------
    draw.text((60, 130), "Structured Professional Content", font=heading_font, fill="orange")

    # ---------- MASK BOX ----------
    box_top = 200
    box_bottom = 980

    draw.rectangle(
        [(50, box_top), (width - 50, box_bottom)],
        fill=(15, 18, 60)
    )

    # ---------- TEXT AREA ----------
    sections = parse_sections(text)

    y = box_top + 30

    for title, content in sections:

        # ===== HEADING =====
        draw.text((90, y), title, font=heading_font, fill="orange")
        y += 60

        # ===== CONTENT =====
        for line in content:
            wrapped_lines = textwrap.wrap(line, width=85)

            for wline in wrapped_lines:
                draw.text((120, y), wline, font=text_font, fill="white")
                y += 40

        y += 25  # spacing between sections

        # prevent overflow
        if y > box_bottom - 60:
            break

    # ---------- SAVE ----------
    os.makedirs(output_folder, exist_ok=True)
    path = os.path.join(output_folder, "slide.png")
    img.save(path)

    return path