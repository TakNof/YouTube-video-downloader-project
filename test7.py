from tkinter.ttk import Progressbar
from tkinter import HORIZONTAL
from pytube import Playlist
from pytube import YouTube
import tkinter as tk
import os
import time
import sys
from threading import Thread, Event
import cProfile

#This test has implemented successfully the optimization with separated threads for the download process and the GUI
#resulting on a better processing of the download process. There might be some errors that could occur owing to this,
#they will be found and solved properly.

#Errors found:
#When pressing the download button once a previous donwload has started.
#When closing the download window.

def show_download_progress(stream, chunk: bytes, bytes_remaining: int):
    if not stop_event.is_set():
        global file_size
        if file_size == 0:
            file_size = bytes_remaining
            
        download_state = round((file_size - bytes_remaining)*100/file_size, 2)
        
        global download_bar
        global download_window
        download_bar['value'] = download_state
        print("Downloading...")
        print(f"{download_state}%")
        print(thr.is_alive())
        download_window.update_idletasks()
    else:
        sys.exit()
        

def show_download_completed(stream, path: str):
    print("\nDownload complete.\n")
    download_window.bell()
    
def download():
    global download_window
    download_window = tk.Toplevel()
    download_window.geometry(newGeometry="700x700")
    
    global download_bar
    download_bar = Progressbar(download_window, orient= HORIZONTAL)
    download_bar.pack(fill="x")
    
    download_window.protocol("WM_DELETE_WINDOW", stop_thread)
    
    download_window.after(300, download_process_thread)

def download_process_thread():
    print(thr.is_alive())
    if not thr.is_alive():  
        thr.start()
        stop_event.clear()
    else:
        thr.run()
                
def stop_thread():
    if thr.is_alive():
        stop_event.set()
        print(thr.is_alive())
    
    download_window.destroy()   

#download_process("https://www.youtube.com/watch?v=iM3kjbbKHQU&t")
#https://www.youtube.com/watch?v=iM3kjbbKHQU&t
#https://www.youtube.com/playlist?list=PLm2GllkbPBKioaJI9Mjazr9uKAEGzId67
#https://www.youtube.com/playlist?list=PLzxRtqFRLWZ892ytyZ2E189Oeaan2m9c4
    
def download_process(url: str):
    video = YouTube(url)
    download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))

    video.register_on_progress_callback(show_download_progress)
    video.register_on_complete_callback(show_download_completed)
    
    global file_size
    file_size = 0
    video.streams.get_highest_resolution().download(download_path)    
    
def main():
    main_window = tk.Tk()
    
    global thr
    thr = Thread(target= download_process, args=("https://www.youtube.com/watch?v=ivl5-snqul8",))
    
    global stop_event
    stop_event = Event()
    
    button = tk.Button(main_window, text="Download", font= "Sans-serif 8", command=download)
    button.pack()
    main_window.mainloop()
    
if __name__ == "__main__":
    st = time.process_time()
    #main()
    cProfile.run('main()', sort='tottime')
    et = time.process_time()
    res = et - st
    if res >= 60:
        print(f"All the downloads have finished in {res/60} minutes.")
    else:
        print(f"All the downloads have finished in {res} seconds.")