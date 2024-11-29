## presso.py ##
## by Behzad Attari ##
## https://github.com/BehzadAttari/presso-desktop ##
## 2024-11-29 ##
## MIT License ##
## v1.0.0 ##


import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import webbrowser
import json
import tkinter as tk
from tkinter import font as tkfont
import sys

# Language strings
LANGUAGES = {
    "English": {
        "input_folder": "Input Folder:",
        "output_folder": "Output Folder:", 
        "browse": "Browse",
        "compress_jpg": "Compress JPG",
        "compress_png": "Compress PNG",
        "quality": "JPG Compression Quality:",
        "worst": "Worst",
        "best": "Best",
        "start": "Start Compression",
        "github": "⭐ If you enjoyed using this, star it on GitHub!",
        "error_dirs": "Please select both input and output directories.",
        "error_types": "Please enable at least one file type for compression.",
        "success": "Compression Completed!\nTotal space saved: {:.2f} MB",
        "rtl": False,
        "font": None,
        "about_title": "About",
        "about_message": "⭐ If you enjoyed using this, star it on GitHub!\n\nIn Memory of Dear Saber Rastikerdar\nWhich his work for the persian opensource community is unforgettable"
    },
    "Farsi": {
        "input_folder": ":پوشه ورودی",
        "output_folder": ":پوشه خروجی",
        "browse": "انتخاب",
        "compress_jpg": "JPG فشرده سازی",
        "compress_png": "PNG فشرده سازی", 
        "quality": ":JPG کیفیت فشرده سازی",
        "worst": "بدترین",
        "best": "بهترین",
        "start": "شروع فشرده سازی",
        "github": "!اگر از این برنامه لذت بردید، به ما در گیت هاب ستاره بدهید ⭐",
        "error_dirs": ".لطفا هر دو پوشه ورودی و خروجی را انتخاب کنید",
        "error_types": ".لطفا حداقل یک نوع فایل را برای فشرده سازی فعال کنید",
        "success": "!فشرده سازی تکمیل شد\nMB {:.2f} :فضای ذخیره شده",
        "rtl": True,
        "font": "Tahoma",
        "about_title": "درباره",
        "about_message": "!اگر از این برنامه لذت بردید، به ما در گیت هاب ستاره بدهید ⭐\n\nبه یاد صابر راستی کردار عزیز\nکه زحماتش برای جامعه برنامه نویسان متن باز ایرانی به یاد ماندنیست"
    }
}

def change_language(lang):
    current_lang.set(lang)
    # Update all text elements
    input_label.configure(text=LANGUAGES[lang]["input_folder"])
    input_browse_btn.configure(text=LANGUAGES[lang]["browse"])
    output_label.configure(text=LANGUAGES[lang]["output_folder"]) 
    output_browse_btn.configure(text=LANGUAGES[lang]["browse"])
    jpg_checkbox.configure(text=LANGUAGES[lang]["compress_jpg"])
    png_checkbox.configure(text=LANGUAGES[lang]["compress_png"])
    quality_label.configure(text=LANGUAGES[lang]["quality"])
    worst_label.configure(text=LANGUAGES[lang]["worst"])
    best_label.configure(text=LANGUAGES[lang]["best"])
    start_button.configure(text=LANGUAGES[lang]["start"])
    
    # Reset to default fonts first
    default_font = ctk.CTkFont(family="Tahoma", size=12)
    default_font_small = ctk.CTkFont(family="Tahoma", size=10)

    # Apply fonts for both languages
    input_label.configure(font=default_font)
    output_label.configure(font=default_font)
    quality_label.configure(font=default_font)
    start_button.configure(font=default_font)

    jpg_checkbox.configure(font=default_font_small)
    png_checkbox.configure(font=default_font_small)
    worst_label.configure(font=default_font_small)
    best_label.configure(font=default_font_small)
    input_browse_btn.configure(font=default_font_small)
    output_browse_btn.configure(font=default_font_small)
    
    if lang == "English":
        app.tk.call("tk", "scaling", 1.0)
        app.configure(width=450)
    else:  # Farsi
        app.tk.call("tk", "scaling", 2.0)
        app.configure(width=450)

# Function to compress images
def compress_images(input_dir, output_dir, quality=80, compress_jpg=True, compress_png=True):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of files for progress bar
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total_files = len(files)
    processed_files = 0
    total_saved = 0

    progress_bar.set(0)
    progress_label.configure(text="0%")

    for file_name in files:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)
        original_size = os.path.getsize(input_path)

        try:
            # Process JPG files
            if (file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg')) and compress_jpg:
                with Image.open(input_path) as img:
                    img.save(output_path, 'JPEG', quality=quality)
                print(f"Compressed JPG: {file_name}")

            # Process PNG files
            elif file_name.lower().endswith('.png') and compress_png:
                with Image.open(input_path) as img:
                    img.save(output_path, 'PNG', optimize=True)
                print(f"Compressed PNG: {file_name}")
            else:
                # Copy file without compression if format is disabled
                import shutil
                shutil.copy2(input_path, output_path)

            # Calculate size reduction
            compressed_size = os.path.getsize(output_path)
            saved = original_size - compressed_size
            total_saved += saved

        except Exception as e:
            print(f"Error compressing {file_name}: {e}")

        # Update progress
        processed_files += 1
        progress = processed_files / total_files
        progress_bar.set(progress)
        progress_label.configure(text=f"{int(progress * 100)}%")
        app.update()

    return total_saved

# Functions for directory selection
def select_input_dir():
    folder = filedialog.askdirectory(title="Select Input Folder")
    if folder:
        input_dir_var.set(folder)

def select_output_dir():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_dir_var.set(folder)

# Start the compression process
def start_compression():
    input_dir = input_dir_var.get()
    output_dir = output_dir_var.get()
    quality = int(quality_var.get())

    if not input_dir or not output_dir:
        messagebox.showerror("Error", LANGUAGES[current_lang.get()]["error_dirs"])
        return

    compress_jpg = jpg_var.get()
    compress_png = png_var.get()

    if not compress_jpg and not compress_png:
        messagebox.showerror("Error", LANGUAGES[current_lang.get()]["error_types"])
        return

    total_saved = compress_images(input_dir, output_dir, quality, compress_jpg, compress_png)
    saved_mb = total_saved / (1024 * 1024)  # Convert to MB
    messagebox.showinfo("Success", LANGUAGES[current_lang.get()]["success"].format(saved_mb))

# Track if about window is open
about_window = None

def show_about():
    global about_window
    
    # If about window exists and is open, just lift it and return
    if about_window is not None and about_window.winfo_exists():
        about_window.lift()
        about_window.focus_force()
        return
        
    about_window = ctk.CTkToplevel(app)
    about_window.title(LANGUAGES[current_lang.get()]["about_title"])
    about_window.geometry("420x550")
    about_window.resizable(False, False)
    about_window.transient(app)
    about_window.grab_set()
    
    # Use the same icon as main window
    about_window.iconbitmap(icon_path)
    about_window.wm_iconphoto(False, icon_photo)
    
    # Create main frame with padding
    main_frame = ctk.CTkFrame(about_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title with Tahoma font
    title_font = ctk.CTkFont(family="Tahoma", size=16, weight="bold")
    title_label = ctk.CTkLabel(
        main_frame, 
        text="Presso",
        font=title_font
    )
    title_label.pack(pady=(0, 20))
    
    # Create a black frame for gif and text
    black_frame = ctk.CTkFrame(main_frame, fg_color="black")
    black_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Message with Tahoma font
    message_font = ctk.CTkFont(family="Tahoma", size=12)
    
    # First line (GitHub section)
    message_label = ctk.CTkLabel(
        black_frame, 
        text=LANGUAGES[current_lang.get()]["about_message"].split('\n')[0],
        wraplength=350,
        font=message_font,
        justify="center",
        text_color="white"
    )
    message_label.pack(pady=(0, 20))
    
    # Second line 
    memorial_label = ctk.CTkLabel(
        black_frame,
        text=LANGUAGES[current_lang.get()]["about_message"].split('\n')[1],
        wraplength=350,
        font=message_font,
        justify="center",
        text_color="white"
    )
    memorial_label.pack(pady=(0, 20))
    
    # Third line 🕊️ 
    work_label = ctk.CTkLabel(
        black_frame,
        text=LANGUAGES[current_lang.get()]["about_message"].split('\n')[2],
        wraplength=350,
        font=message_font,
        justify="center",
        text_color="white"
    )
    work_label.pack(pady=(0, 20))
    
    # Load and display animated gif
    try:
        gif_path = os.path.join(application_path, "candle.gif")
        gif = Image.open(gif_path)
        frames = []
        for frame in range(0, gif.n_frames):
            gif.seek(frame)
            frames.append(ctk.CTkImage(gif.copy(), size=(150, 150)))
        
        gif_label = ctk.CTkLabel(black_frame, image=frames[0], text="", cursor="hand2")
        gif_label.pack(pady=(0, 10))
        gif_label.bind("<Button-1>", lambda e: webbrowser.open("https://rastikerdar.github.io/"))
        
        def animate(frame_index=0):
            gif_label.configure(image=frames[frame_index])
            next_frame = (frame_index + 1) % len(frames)
            black_frame.after(50, animate, next_frame)
            
        animate()
    except Exception as e:
        print(f"Error loading animated gif: {e}")
    
    # Fourth line 
    work_label = ctk.CTkLabel(
        black_frame,
        text=LANGUAGES[current_lang.get()]["about_message"].split('\n')[3],
        wraplength=350,
        font=message_font,
        justify="center",
        text_color="white"
    )
    work_label.pack(pady=(10, 20))
    
    # Separator
    separator = ctk.CTkFrame(main_frame, height=2)
    separator.pack(fill="x", pady=(0, 20))
    
    # GitHub button
    github_button = ctk.CTkButton(
        main_frame,
        text="Visit GitHub ↗",
        font=message_font,
        command=lambda: webbrowser.open("https://github.com/BehzadAttari/presso-desktop"),
        height=35,
        corner_radius=8
    )
    github_button.pack(pady=(0, 10))

# Initialize the customtkinter app
ctk.set_appearance_mode("Light")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Available themes: "blue", "green", "dark-blue"

app = ctk.CTk()
app.title("Presso")
app.geometry("450x550")

# Add icon to the window
try:
    # Handle both compiled exe and script scenarios
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        
    icon_path = os.path.join(application_path, "icon.ico")  # for Windows
    app.iconbitmap(icon_path)
    
    # For Linux/Mac support (optional)
    icon_img = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_img)
    app.wm_iconphoto(True, icon_photo)
except Exception as e:
    print(f"Error loading icon: {e}")

# Current language
current_lang = tk.StringVar(value="English")

# Create menubar
menubar = tk.Menu(app)
app.configure(menu=menubar)

# Create Settings menu
settings_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Settings", menu=settings_menu)

# Add About menu
menubar.add_command(label="About", command=show_about)

# Add language menu items
settings_menu.add_radiobutton(
    label="English",
    command=lambda: change_language("English"),
    variable=current_lang,
    value="English"
)
settings_menu.add_radiobutton(
    label="Farsi",
    command=lambda: change_language("Farsi"),
    variable=current_lang,
    value="Farsi"
)

# Input Directory
input_dir_var = ctk.StringVar()
input_label = ctk.CTkLabel(app, text=LANGUAGES[current_lang.get()]["input_folder"])
input_label.pack(pady=(20, 5))
ctk.CTkEntry(app, textvariable=input_dir_var, width=400).pack(pady=5)
input_browse_btn = ctk.CTkButton(app, text=LANGUAGES[current_lang.get()]["browse"], command=select_input_dir)
input_browse_btn.pack(pady=5)

# Output Directory
output_dir_var = ctk.StringVar()
output_label = ctk.CTkLabel(app, text=LANGUAGES[current_lang.get()]["output_folder"])
output_label.pack(pady=5)
ctk.CTkEntry(app, textvariable=output_dir_var, width=400).pack(pady=5)
output_browse_btn = ctk.CTkButton(app, text=LANGUAGES[current_lang.get()]["browse"], command=select_output_dir)
output_browse_btn.pack(pady=5)

# File type toggles
jpg_var = ctk.BooleanVar(value=True)
png_var = ctk.BooleanVar(value=True)
toggle_frame = ctk.CTkFrame(app)
toggle_frame.pack(pady=10)
jpg_checkbox = ctk.CTkCheckBox(toggle_frame, text=LANGUAGES[current_lang.get()]["compress_jpg"], variable=jpg_var)
jpg_checkbox.pack(side="left", padx=10)
png_checkbox = ctk.CTkCheckBox(toggle_frame, text=LANGUAGES[current_lang.get()]["compress_png"], variable=png_var)
png_checkbox.pack(side="left", padx=10)

# Compression Quality Slider
quality_var = ctk.IntVar(value=80)
quality_label = ctk.CTkLabel(app, text=LANGUAGES[current_lang.get()]["quality"])
quality_label.pack(pady=5)
slider_frame = ctk.CTkFrame(app)
slider_frame.pack(pady=5)
worst_label = ctk.CTkLabel(slider_frame, text=LANGUAGES[current_lang.get()]["worst"], text_color="red")
worst_label.pack(side="left", padx=5)
quality_slider = ctk.CTkSlider(slider_frame, from_=1, to=100, variable=quality_var, width=300)
quality_slider.pack(side="left", padx=5)
best_label = ctk.CTkLabel(slider_frame, text=LANGUAGES[current_lang.get()]["best"], text_color="green")
best_label.pack(side="left", padx=5)
quality_value_label = ctk.CTkLabel(app, textvariable=quality_var)
quality_value_label.pack(pady=(0, 10))

# Progress Bar
progress_frame = ctk.CTkFrame(app)
progress_frame.pack(pady=10, fill="x", padx=20)
progress_bar = ctk.CTkProgressBar(progress_frame)
progress_bar.pack(pady=5, fill="x")
progress_bar.set(0)
progress_label = ctk.CTkLabel(progress_frame, text="0%")
progress_label.pack()

# Start Button
start_button = ctk.CTkButton(app, text=LANGUAGES[current_lang.get()]["start"], command=start_compression)
start_button.pack(pady=20)

# Run the App
app.mainloop()
