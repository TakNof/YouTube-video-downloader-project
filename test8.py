import os
import time
import tkinter as tk

from multiprocessing.pool import ThreadPool as Pool
from pytube import Playlist
from pytube import YouTube
from tkinter.ttk import Progressbar
from tkinter import END, HORIZONTAL, BooleanVar, PhotoImage, StringVar, filedialog, messagebox

#This test will be used to try the procedure of multiple downloads at once, with their corresponding donwload bars
#and indicators.

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
    
def show_download_window():
    global download_window
    download_window = tk.Toplevel()
    download_window.geometry(newGeometry="700x700")
    
    #The main label.
    download_label = tk.Label(download_window, text= "Downloading...", font=("Sans-serif", 16), justify="center")
    download_label.pack()
    
    #The main progress bar.
    global main_progress_bar    
    main_progress_bar = Progressbar(download_window, orient= HORIZONTAL)
    main_progress_bar.pack(fill="x")
    
    #The percentage of progress of the download.
    global percentage_download
    #Owing to the fact that the percentage of progress has to change through time it has to be stablished in this way.
    percentage_download = StringVar()
    percentage_download.set("Starting download...") 
    percentage_download_label = tk.Label(download_window, textvariable= percentage_download)
    percentage_download_label.pack()
        
    for i in range(playlist_length):
        #The bytes downloaded.
        global bytes_downloaded
        #Owing to the fact that the bytes downloaded changes through time it has to be stablished in this way.
        bytes_downloaded = StringVar()
        bytes_downloaded_label = tk.Label(download_window, textvariable= bytes_downloaded)
        bytes_downloaded_label.pack()
        
        #The task progress bar in case of donwloading a playlist.
        global task_progress_bar    
        task_progress_bar = Progressbar(download_window, orient= HORIZONTAL)
        task_progress_bar.pack(fill="x")
            
    #The amount of tasks downloaded.
    global tasks_completed
    #Owing to the fact that the amount of tasks completed have to change through time it has to be stablished in this way.
    tasks_completed = StringVar()
    tasks_completed.set("Loading elements...")
    tasks_completed_label = tk.Label(download_window, textvariable= tasks_completed)
    tasks_completed_label.pack()
        
    #The total amount of bytes downloaded of the group of files.
    global total_bytes_downloaded
    #Owing to the fact that the bytes downloaded changes through time it has to be stablished in this way.
    total_bytes_downloaded = StringVar()
    total_bytes_downloaded_label = tk.Label(download_window, textvariable= total_bytes_downloaded)
    total_bytes_downloaded_label.pack()

    #The label that indicates that the download has finished successfully.
    global download_complete_label
    download_complete_label = tk.Label(download_window, text= "", font=("Sans-serif", 16), justify="center")
    download_complete_label.pack()
    
    #download_window.after(300, lambda: download_process("https://www.youtube.com/playlist?list=PLzxRtqFRLWZ892ytyZ2E189Oeaan2m9c4"))

def download_process(url: str):
    pool_size = playlist_length
        
    pool = Pool(pool_size)
    global pl
    
    global file_size_list
    file_size_list = [0] * pool_size
    
    for num, video in enumerate(pl.videos, start= 1):
        pool.apply_async(download, (video, num,))
        
        
    pool.close()
    pool.join()
        

def download(video: YouTube, num: int):
    video.register_on_progress_callback(show_download_progress)
    video.register_on_complete_callback(show_download_completed)
        
    print(f"downloading video #{num}.")
    video.streams.get_highest_resolution().download(download_path)
    print(f"video #{num} donwloaded.")
        
def main():
    main_window = tk.Tk()
    
    global url
    url = "https://www.youtube.com/playlist?list=PLzxRtqFRLWZ892ytyZ2E189Oeaan2m9c4"

    global download_path
    download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))
    
    global pl
    pl = Playlist(url)

    global playlist_length
    playlist_length = len(pl.videos)

    button = tk.Button(main_window, text="Download", font= "Sans-serif 8", command=show_download_window)
    button.pack()
    main_window.mainloop()
                
if __name__ == "__main__":
               
    st = time.process_time()
    
    main()
    et = time.process_time()
    res = et - st
        
    if res >= 60: 
        print(f"All the downloads have finished in {res/60} minutes.")
    else:
        print(f"All the downloads have finished in {res} seconds.")
    