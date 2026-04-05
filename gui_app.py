import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

from modules.file_reader import read_file
from modules.gemini_processor import process_text
from modules.slide_generator import create_single_slide
from modules.voice_generator import generate_voice
from modules.video_creator import create_video


# ---------- WINDOW ----------
root = tk.Tk()
root.title("🔥 AI Video Generator PRO")
root.geometry("900x650")
root.configure(bg="#0f172a")

file_path = ""
output_folder = "outputs"
language = "en"


# ---------- STYLE ----------
style = ttk.Style()
style.theme_use("clam")

style.configure("TProgressbar",
                thickness=15,
                background="#22c55e")


# ---------- FUNCTIONS ----------

def select_file():
    global file_path
    path = filedialog.askopenfilename(
        filetypes=[("Documents", "*.pdf *.docx *.txt")]
    )
    if path:
        file_path = path
        file_label.config(text=path, fg="#38bdf8")


def select_language(lang):
    global language
    language = lang
    status_label.config(text=f"Language Selected: {lang.upper()}")


def update_status(msg):
    status_label.config(text=msg)
    root.update()


def run_process():

    if not file_path:
        messagebox.showerror("Error", "Please select a file")
        return

    try:
        progress.start()

        # ---------- READ ----------
        update_status("📄 Reading Document...")
        text = read_file(file_path)

        if not text.strip():
            raise Exception("Empty file or unreadable content")

        # ---------- AI PROCESS ----------
        update_status("🤖 AI Processing...")
        processed = process_text(text, language)

        # ---------- SLIDE ----------
        update_status("🖼️ Creating Slide...")
        create_single_slide(processed, output_folder)

        # ---------- VOICE ----------
        update_status("🔊 Generating Voice...")
        audio_path = generate_voice(processed, output_folder, language)

        # ---------- VIDEO ----------
        update_status("🎬 Creating Video...")
        video_path = os.path.join(output_folder, "final_video.mp4")
        create_video(processed, audio_path, video_path)

        progress.stop()
        update_status("✅ Completed Successfully!")

        messagebox.showinfo("Success", "Video Generated Successfully 🎉")

        os.startfile(video_path)

    except Exception as e:
        progress.stop()
        messagebox.showerror("Error", str(e))


def start_thread():
    thread = threading.Thread(target=run_process)
    thread.start()


# ---------- UI DESIGN ----------

# Title
title = tk.Label(root,
                 text="🚀 AI Resume / Document Video Generator",
                 font=("Arial", 24, "bold"),
                 fg="#22c55e",
                 bg="#0f172a")
title.pack(pady=20)

# File Button
btn_file = tk.Button(root,
                     text="📄 Select Document",
                     font=("Arial", 14, "bold"),
                     bg="#3b82f6",
                     fg="white",
                     padx=10,
                     pady=5,
                     command=select_file)
btn_file.pack(pady=10)

file_label = tk.Label(root,
                      text="No file selected",
                      fg="white",
                      bg="#0f172a")
file_label.pack()

# Language Selection
lang_frame = tk.Frame(root, bg="#0f172a")
lang_frame.pack(pady=20)

tk.Label(lang_frame,
         text="🌐 Select Language:",
         font=("Arial", 12, "bold"),
         fg="white",
         bg="#0f172a").pack(side="left", padx=10)

btn_en = tk.Button(lang_frame,
                   text="English",
                   bg="#22c55e",
                   fg="black",
                   command=lambda: select_language("en"))
btn_en.pack(side="left", padx=10)

btn_hi = tk.Button(lang_frame,
                   text="Hindi",
                   bg="#f97316",
                   fg="black",
                   command=lambda: select_language("hi"))
btn_hi.pack(side="left", padx=10)

# Generate Button
generate_btn = tk.Button(root,
                         text="🚀 Generate Video",
                         font=("Arial", 16, "bold"),
                         bg="#22c55e",
                         fg="black",
                         padx=20,
                         pady=10,
                         command=start_thread)
generate_btn.pack(pady=30)

# Progress Bar
progress = ttk.Progressbar(root, mode="indeterminate")
progress.pack(pady=10, fill="x", padx=80)

# Status Label
status_label = tk.Label(root,
                        text="Ready",
                        font=("Arial", 12),
                        fg="#eab308",
                        bg="#0f172a")
status_label.pack(pady=15)

# Footer
footer = tk.Label(root,
                  text="⚡ Powered by AI Automation",
                  fg="#64748b",
                  bg="#0f172a")
footer.pack(side="bottom", pady=10)

# ---------- RUN ----------
root.mainloop()