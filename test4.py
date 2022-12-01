import os
import time
from pytube import Playlist
from pytube import YouTube

#This is the regular procedure to download all the videos from a playlist.
#The time this procedure lasts does not take on account the time of the gui loading process.
#With the playlist of 3 videos: 32.8 seconds

def download(video: YouTube, num: int):
    print(f"downloading video #{num}.")
    video.streams.get_highest_resolution().download(download_path)
    print(f"video #{num} donwloaded.")

st = time.process_time()

url = "https://www.youtube.com/playlist?list=PLm2GllkbPBKioaJI9Mjazr9uKAEGzId67"

global download_path
download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))

pl = Playlist(url)

for num, video in enumerate(pl.videos, start= 1):
    download(video, num)
    
et = time.process_time()
res = et - st

if res >= 60:
        print(f"All the downloads have finished in {res/60} minutes.")
else:
    print(f"All the downloads have finished in {res} seconds.")