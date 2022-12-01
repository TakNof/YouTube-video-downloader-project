import os
import time
from multiprocessing.pool import ThreadPool as Pool
from pytube import Playlist
from pytube import YouTube

#This method turned out to have similar performance as the original process. However,
#this one lasts 2 seconds longer than the original process. More benchmarking should be
#done in order to check if is there a case where performance is better than the original.

def download(video: YouTube, num: int):
    video_titles.append(video.title)
    print(f"downloading video #{num}.")
    video.streams.get_highest_resolution().download(download_path)
    print(f"video #{num} donwloaded.")
        
def main():
    url = "https://www.youtube.com/watch?v=VlWyaYyYXNg&list=RDMM&start_radio=1&rv=1Zrq8FiKS6A"

    global download_path
    download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))
    
    pl = Playlist(url)

    global video_titles
    video_titles = []
        
    global playlist_length
    playlist_length = len(pl.videos)
    
    pool_size = playlist_length
        
    pool = Pool(pool_size)

    for num, video in enumerate(pl.videos, start= 1):
        pool.apply_async(download, (video, num,))
        
        
    pool.close()
    pool.join()
            
if __name__ == "__main__":
    #for i in range(2,22,2):
                
        st = time.process_time()
    
        main()
        et = time.process_time()
        res = et - st
        
        if res >= 60: 
            print(f"All the downloads have finished in {res/60} minutes.")
        else:
            print(f"All the downloads have finished in {res} seconds.")
            
        #for i in range(0, playlist_length):
        #    try:
        #        os.remove(os.path.join(download_path, video_titles[i]+".mp4"))
        #    except Exception:
        #        pass