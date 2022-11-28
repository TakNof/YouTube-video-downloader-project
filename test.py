from tkinter.ttk import Progressbar
from tkinter import HORIZONTAL
from pytube import Playlist
import tkinter as tk
import os
import time
import threading
from multiprocessing import Process
import cProfile

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
    download_window.bell()
    
def download():
    global download_window
    download_window = tk.Toplevel()
    download_window.geometry(newGeometry="700x700")
    
    global download_bar
    download_bar = Progressbar(download_window, orient= HORIZONTAL, length= 300)
    download_bar.pack()
    
    download_window.after(300, lambda: download_process("https://www.youtube.com/playlist?list=PLzxRtqFRLWZ892ytyZ2E189Oeaan2m9c4"))
    
#https://www.youtube.com/playlist?list=PLm2GllkbPBKioaJI9Mjazr9uKAEGzId67
    
def download_process(url: str):
    pl = Playlist(url)
    download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))

    for video in pl.videos:
        video.register_on_progress_callback(show_download_progress)
        video.register_on_complete_callback(show_download_completed)
    
        global file_size
        file_size = 0
        video.streams.get_highest_resolution().download(download_path)

def call_download_method():
    prcs2 = Process(target= download())
    prcs2.start()
    prcs2.join()  
    
def call_download_process_method(url: str):
    thr2 = threading.Thread(target= download_process, args=(url,))
    thr2.start()
    
    
def call_show_download_progress_method(stream, chunk: bytes, bytes_remaining: int):
    thr3 = threading.Thread(target= show_download_progress, args=(stream, chunk, bytes_remaining,))
    thr3.start()
  
    
def call_show_download_completed_method(stream, path: str):
    thr4 = threading.Thread(target= show_download_completed, args=(stream, path,))
    thr4.start()
    
    
def main():
    main_window = tk.Tk() 

    button = tk.Button(main_window, text="Download", font= "Sans-serif 8", command=call_download_method)
    button.pack()
    main_window.mainloop()
    
def call_main_method():
    prcs1 = Process(target= main())
    prcs1.start()
        
if __name__ == "__main__":
    #main()
    cProfile.run('call_main_method()', sort='tottime')
    print(time.perf_counter())
    