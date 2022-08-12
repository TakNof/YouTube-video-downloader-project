from tkinter.ttk import Progressbar
from tkinter import HORIZONTAL
from pytube import YouTube
import tkinter as tk
import time

def show_download_progress(stream, chunk: bytes, bytes_remaining: int):
    global file_size
    if file_size == 0:
        file_size = bytes_remaining
        
    download_state = round((file_size - bytes_remaining)*100/file_size, 2)
    
    global download_bar
    global download_window
    download_bar['value'] = download_state
    print("Downloading...")
    print(f"{download_state}%")
    download_window.update_idletasks()

def show_download_completed(stream, path: str):
    print("\nDownload complete.\n")
    
def download():
    global download_window
    download_window = tk.Toplevel()
    download_window.geometry(newGeometry="700x700")
    
    global download_bar
    download_bar = Progressbar(download_window, orient= HORIZONTAL, length= 300)
    download_bar.pack()
    
    download_window.after(300, download_process)
    
    
    
def download_process():
    yt = YouTube("https://www.youtube.com/watch?v=iKVrx5Vx1rs")

    yt.register_on_progress_callback(show_download_progress)
    yt.register_on_complete_callback(show_download_completed)

    global file_size
    file_size = 0
    yt.streams.get_audio_only().download()
    
    
main_window = tk.Tk() 

button = tk.Button(main_window, text="Download", font= "Sans-serif 8", command=download)
button.pack()

main_window.mainloop()
