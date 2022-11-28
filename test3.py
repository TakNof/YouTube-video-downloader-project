import os
import time
from multiprocessing.pool import ThreadPool as Pool
from pytube import Playlist
from pytube import YouTube

def download(video: YouTube, num: int):
    print(f"downloading video #{num}.")
    video.streams.get_highest_resolution().download(download_path)
    print(f"video #{num} donwloaded.")
    
url = "https://www.youtube.com/playlist?list=PLm2GllkbPBKioaJI9Mjazr9uKAEGzId67"

global download_path
download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))

pl = Playlist(url)

if len(pl.videos) >= 10:
    pool_size = 10
else:
    pool_size = len(pl.videos)
    
pool = Pool(pool_size)
for num, video in enumerate(pl.videos, start= 1):
    pool.apply_async(download, (video, num,))
    
pool.close()
pool.join()
print(f"All the downloads have finished in {time.perf_counter()/935.025} minutes.")