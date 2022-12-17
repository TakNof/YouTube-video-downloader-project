import os
import time
import multiprocessing
import cProfile
from pytube import Playlist
from pytube import YouTube

#Notes, this method showed not to be useful. It is highly inefficient and it can easily colapse
#the pc CPU. The more videos are in the playlist, the more processes are created into the array, thus 
#when exceding the amount of available cores of the cpu, all the prcesses start to colapse the full system.

#Even taking less amount of videos through the playlist it stills being very unefficient, it turns out to be
#actually slower than the original procedure.

def download(video: YouTube, num: int):
    download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))
    print(f"downloading video #{num}.")
    video.streams.get_highest_resolution().download(download_path)
    print(f"video #{num} donwloaded.")
    
def main():
    url = "https://www.youtube.com/playlist?list=PLm2GllkbPBKioaJI9Mjazr9uKAEGzId67"
    
    pl = Playlist(url)

    processes = [multiprocessing.Process(target= download, args= (video, num,)) for num, video in enumerate(pl.videos, start= 1)]
    
    for processi in processes:
        processi.start()
        
        
    for processi in processes:
        processi.join()
            
if __name__ == "__main__":   
    #main()
    cProfile.run('main()', sort='tottime')
    