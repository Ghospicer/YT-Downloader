import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import os
import subprocess

# Function to check if ffmpeg is installed
def check_ffmpeg_installed():
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')
    if os.path.isfile(ffmpeg_path):
        try:
            result = subprocess.run([ffmpeg_path, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return True
            else:
                print("Error output:", result.stderr)
                return False
        except FileNotFoundError as e:
            print("FFmpeg not found:", e)
            return False
    else:
        print("FFmpeg executable not found.")
        return False

# Function to download video or audio
def download_video(url, download_type, quality, progress_var):
    if not check_ffmpeg_installed():
        messagebox.showerror("Error", "FFmpeg is not installed. Please install FFmpeg to handle video and audio merging.")
        return

    def update_progress(d):
        if d['status'] == 'finished':
            progress_var.set(100)
        elif d['status'] == 'downloading':
            progress_var.set(int((d['downloaded_bytes'] / d['total_bytes']) * 100))
        root.update_idletasks()

    try:
        # Define format selection based on quality
        format_selection = {
            '360p': 'bestvideo[height<=360]+bestaudio/best',
            '480p': 'bestvideo[height<=480]+bestaudio/best',
            '720p': 'bestvideo[height<=720]+bestaudio/best',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best',
            '1440p': 'bestvideo[height<=1440]+bestaudio/best',
            '2K': 'bestvideo[height<=2160]+bestaudio/best'
        }
        
        format_code = format_selection.get(quality, 'bestvideo+bestaudio')

        # Set up options for yt_dlp
        ydl_opts = {
            'format': format_code if download_type == "MP4" else 'bestaudio/best',
            'outtmpl': os.path.join(filedialog.askdirectory(), '%(title)s.%(ext)s'),
            'progress_hooks': [update_progress]
        }
        
        if download_type == "MP3":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        # Create a YoutubeDL instance
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("Success", f"Downloaded {url} as {download_type} with {quality} quality")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle button click and start download
def start_download():
    url = url_entry.get()
    download_type = download_type_var.get()
    quality = quality_var.get()
    
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    
    progress_var.set(0)  # Reset progress bar
    download_video(url, download_type, quality, progress_var)

# Creating the UI
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x400")  # Adjusted window size
root.configure(bg="#f0f0f0")

# YouTube URL input
url_label = tk.Label(root, text="YouTube URL:", bg="#f0f0f0", font=("Arial", 12))
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=40, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Download type selection
download_type_var = tk.StringVar(value="MP4")
download_type_frame = tk.Frame(root, bg="#f0f0f0")
download_type_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")
mp4_radio = tk.Radiobutton(download_type_frame, text="MP4", variable=download_type_var, value="MP4", bg="#f0f0f0", font=("Arial", 12))
mp3_radio = tk.Radiobutton(download_type_frame, text="MP3", variable=download_type_var, value="MP3", bg="#f0f0f0", font=("Arial", 12))
mp4_radio.pack(side=tk.LEFT, padx=10)
mp3_radio.pack(side=tk.LEFT)

# Quality selection
quality_var = tk.StringVar(value="720p")
quality_label = tk.Label(root, text="Quality:", bg="#f0f0f0", font=("Arial", 12))
quality_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
quality_options = ['360p', '480p', '720p', '1080p', '1440p', '2K']
quality_menu = tk.OptionMenu(root, quality_var, *quality_options)
quality_menu.config(font=("Arial", 12), width=10)
quality_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.grid(row=3, column=0, columnspan=2, pady=20)

# Download button
download_button = tk.Button(root, text="Download", command=start_download, font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.RAISED, padx=10, pady=5)
download_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
