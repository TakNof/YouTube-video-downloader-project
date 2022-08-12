import os
from pytube import YouTube

class youtube_downloader:
    """
    The youtube_downloader class allows the user to download a video from a YouTube channel
    using the pytube API
    
    when creating an object of this class, you will be able to set the basic properties through
    the video link attribute.
    """
    url: str
    """
    The url of the video to be downloaded.
    """
    video: YouTube
    """
    The YouTube object.
    """
    download_file_name: str
    """
    The name the file of the video will have when downloaded.
    """
    download_path: str
    """
    The download path where the video will be downloaded.
    """
    
    special_characters = "#$%'*+,./:;=?@[\]^`{|}~\""
    """
    A string that represents the special characters that will be errased from the video name to prevent errors.
    """
    
    def set_url(self, url):
        """
        This method sets the url of the video, automatically setting the YouTube object and the download file name.
        """
        self.url = url
        self.__set_yt_ob()
        self.__set_download_file_name()
            
    def __set_yt_ob(self):
        """
        This method creates de YouTube object.
        """
        self.video = YouTube(self.url)
        
    def __set_download_file_name(self):
        """
        This method sets the name of the file of the video to be downloaded.
        """
        #Due the name of the file of the video comes from the title of the video, we save
        #the title into the variable download_file_name.
        self.download_file_name = self.video.title
        
        #From the donwload_file_name saved previously, we check every character in the filename
        #through a for loop, if a special character is encountered it will be removed.
        for letter in self.video.title:
            if(letter in self.special_characters):
                self.download_file_name = self.download_file_name.replace(letter, '')
    
    def set_download_path(self, path: str):
        """
        This method sets the download path.
        Args:
            path (str): An string with the download path (Absolute path).
        """
        self.download_path = path
        
    def get_download_path(self):
        """
        This method returns the donwload path.
        Returns:
            str: The download path. 
        """
        return self.download_path
    
    def download_video(self, confirmation_open_file: bool):
        """
        This method downloads the saved url video.
        Args:
            confirmation_open_file (bool): a bool indicating wheter to open the file when the download is completed or not.
        """
        
        #Here we indicate we are downloading the video file with the highest quality available,
        #as well as the video download path where it will be located.
        self.video.streams.get_highest_resolution().download(self.download_path)
        
        #Here we add the extention of the video file to the string saving it.
        self.download_file_name = f"{self.download_file_name}.mp4"
        
        #If the confirmation to open the file was True, we call for the open_downloaded_file method.
        if confirmation_open_file is True:
            self.open_downloaded_file()
    
    def download_audio(self, confirmation_open_file: bool):
        """
        This method download the audio of the saved url video.
        Args:
            confirmation_open_file (bool): a bool indicating wether to open the file when the donwload is completed or not.
        """
        
        #Here we indicate we are downloading the video file with the highest quality available,
        #as well as the video download path where it will be located.
        self.video.streams.get_audio_only().download(self.download_path)
        
        #A curious thing is when the audio of the video is downloaded it downloads with .mp4 extension instead of .mp3.
        #Because of that we rename the audio file to .mp3 directly in the system.
        os.rename(f"{self.download_path}\\{self.download_file_name}.mp4", f"{self.download_path}\\{self.download_file_name}.mp3")
        
        #Here we add the extention of the audio file to the string saving it.
        self.download_file_name = f"{self.download_file_name}.mp3"
        
        #If the confirmation to open the file was True, we call for the open_downloaded_file method.
        if confirmation_open_file is True:
            self.open_downloaded_file()
    
    def open_downloaded_file(self):
        """
        This method opens the downloaded file using the download file path and the donwload file name
        """
        os.startfile(self.download_path + "\\" + self.download_file_name)
                
    def get_yt_ob(self):
        """
        This method returns the YouTube object.
        Returns:
            YouTube: A YouTube object representing the video object.
        """
        return self.video
    