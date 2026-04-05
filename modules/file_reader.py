import PyPDF2
import docx
import os


# ---------- CLEAN TEXT ----------
def clean_text(text):
    if not text:
        return ""
    
    # remove extra spaces
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    
    # normalize new lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    return "\n".join(lines)


# ---------- PDF READER ----------
def read_pdf(path):
    if not os.path.exists(path):
        raise FileNotFoundError("PDF file not found")

    text = ""

    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            if not reader.pages:
                return ""

            for page in reader.pages:
                try:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
                except:
                    continue

    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

    return clean_text(text)


# ---------- DOCX READER ----------
def read_docx(path):
    if not os.path.exists(path):
        raise FileNotFoundError("DOCX file not found")

    try:
        doc = docx.Document(path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return clean_text(text)

    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")


# ---------- TXT READER ----------
def read_txt(path):
    if not os.path.exists(path):
        raise FileNotFoundError("TXT file not found")

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return clean_text(text)

    except UnicodeDecodeError:
        # fallback encoding
        with open(path, "r", encoding="latin-1") as f:
            text = f.read()
        return clean_text(text)

    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")


# ---------- AUTO DETECT FILE TYPE ----------
def read_file(path):
    if path.endswith(".pdf"):
        return read_pdf(path)
    elif path.endswith(".docx"):
        return read_docx(path)
    elif path.endswith(".txt"):
        return read_txt(path)
    else:
        raise ValueError("Unsupported file format")