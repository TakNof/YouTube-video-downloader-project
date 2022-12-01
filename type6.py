from pytube import YouTube
import moviepy
import moviepy.editor
import os

download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))

url = "https://www.youtube.com/watch?v=pXnpsBBBMo4"

yt = YouTube(url)

file_name = yt.title

yt.streams.get_audio_only().download(download_path, f"{file_name}.mp3")

#video_file = moviepy.editor.VideoFileClip(os.path.join(download_path, f"{file_name}.mp4"))

#video_file.audio.write_audiofile(os.path.join(download_path, f"{file_name}.mp3"))