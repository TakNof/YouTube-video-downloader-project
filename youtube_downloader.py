import os
from pytube import YouTube
from pytube import Playlist

class youtube_downloader:
    """
    The youtube_downloader class allows the user to download a video from a YouTube channel
    using the pytube API
    
    when creating an object of this class, you will be able to set the basic properties through
    the video link attribute.
    """
    url: str
    """
    The url of the video or playlist to be downloaded.
    """
    video: YouTube
    """
    The YouTube object.
    """
    playlist: Playlist
    """
    The playlist object
    """
    is_playlist: bool
    """
    Boolean indicating whether the url is a playlist or a video.
    """
    
    download_file_name: str
    """
    The name the file of the video will have when downloaded.
    """
    download_path: str
    """
    The download path where the video will be downloaded.
    """
    
    special_characters = "#$%'*+,./:;=?@[]^`{|}~\""
    """
    A string that represents the special characters that will be errased from the video name to prevent errors.
    """
    
    def set_url(self, url):
        """
        This method sets the url of the video, automatically setting the YouTube object and the download file name.
        """
        self.url = url
        
        #Because the user can give an url of a video or of a playlist we have to
        #put a conditional to let the program know which one will be downloaded.
        #If it turns out that is a playlist then we create a playlist object, otherwise
        #we create a YouTube object and we set the name the video will have to be downloaded.
        if "playlist" in self.url or "list" in self.url:
            self.__set_pl_ob()                        
        else:
            self.set_yt_ob()
            self.set_download_file_name()
    
    def __set_pl_ob(self):
        """
        This method creates the Playlist Youtube object.
        """
        self.playlist = Playlist(self.url)
    
    def set_yt_ob(self, is_playlist: bool = False, url: str = None):
        """
        This method creates the YouTube object.
        Args:
            is_playlist (bool, optional): Boolean variable to know whether the url given was a playlist or not. Defaults to False.
            url (str, optional): A string with the url of the video. Defaults to None.
        """
        
        #With the playlists we cannot follow the same process as before, so we
        #create a conditional to separate it slightly, however, this change stills working
        #in both cases thanks to the default settings stablished. With these changes the whole
        #logic created previously is preserved intact. 
        if is_playlist:
            self.video = YouTube(url)
        else:
            self.video = YouTube(self.url)
        
    def set_download_file_name(self):
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
        #Here we add the extention of the video file to the string saving it.
        self.download_file_name = f"{self.download_file_name}.mp4"
        
        #Here we indicate we are downloading the video file with the highest quality available,
        #as well as the video download path where it will be located.
        self.video.streams.get_highest_resolution().download(self.download_path, self.download_file_name)
                
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
        self.video.streams.get_audio_only().download(self.download_path, f"{self.download_file_name}.mp4")
        
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
    
    def get_pl_ob(self):
        """
        This method returns the Playlist object.
        Returns:
            Playlist: A Playlist object representing the youtube playlist object.
        """
        return self.playlist
    
    def get_size_of_file(self,download_audio_only_confirmation: bool, is_playlist: bool = False, url: str = None):
        if is_playlist:
            used_url = url
        else:
            used_url = self.url
            
        if download_audio_only_confirmation is True:
            return YouTube(used_url).streams.get_audio_only().filesize
        else:
            return YouTube(used_url).streams.get_highest_resolution().filesize