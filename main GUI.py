import os
from tkinter import END, HORIZONTAL, BooleanVar, PhotoImage, StringVar, filedialog, messagebox
from tkinter.ttk import Progressbar

import youtube_downloader
import tkinter as tk

def center_element_x(screen_width: int, element_width = 0, type: str = "px"):
    """
    This method is used to center the elements of the canvas.
    Args:
        screen_width (int): The screen witdth in pixels.
        element_width (int, optional): The element width, depending on the units the element uses. Defaults to 0.
        type (str, optional): The type of "units" the element use (Not all the elements use the same type of "units"). Defaults to "px".

    Raises:
        BaseException: The type of units was not found into the available options.

    Returns:
        float: The correct scale of the element according to the specified units and the width of the screen.
    """
    
    #Conditional to know the units, if it could not be found it raises an exception.
    if type == "px":
        return screen_width/2 - element_width/2
    elif type == "un":
        element_width = element_width*10/1.1
        return screen_width/2 - element_width/2
    else:
        raise BaseException("The type argument must be either 'px', 'un' or 'text' ")

def open_options(download_path: str):
    """
    This method opens the options window.
    Args:
        download_path (str): An string with the path to the download file.
    """
    
    #Creating a new window which will be displayed on the top.
    options_window = tk.Toplevel()
    options_window.geometry(str(screen_width) + "x" + str(screen_height))
    
    #A label with the download path will be displayed on the new window, to let the user know where the download will be saved.
    download_path_message = tk.Label(options_window, text=f"The current download folder is:\n{download_path}", font=("consolas", 16), justify="left")
    download_path_message.pack(padx=0)
    
    #Here we set a button to let the user change the download path as they wish.
    change_download_path_button = tk.Button(options_window,
                                            text="Change the download path",
                                            command = lambda: change_download_path(download_path_message),
                                            font=("Consolas", 18))
    change_download_path_button.pack(padx=0)

def set_download_path():
    """
    This method sets the path where the files will be downloaded.
    Returns:
        str: The download path as a string.
    """
    if(os.path.exists(config_file_name) is False):
        with open(config_file_name, "w") as config_file_w:
            config_file_w.write("download_path = None")
            config_file_w.close()
    
    config_file_r = open(config_file_name, 'r')
    read_config_file = config_file_r.readline()
            
    if (read_config_file == "download_path = None"):
                
        config_file_w = open(config_file_name, 'w')
             
        home = os.path.expanduser("~")
        os.path.join(home, "Downloads")   
        download_path = str(os.path.join(home, "Downloads"))
        config_file_w.write("download_path = " + download_path)
        
        return download_path
    else:
        config_file_r.close()
        return read_config_file.split("= ")[-1]

def change_download_path(label: tk.Label):
    new_download_path = filedialog.askdirectory()
    
    global download_path
    if new_download_path != "":
        config_file_w = open(config_file_name, 'w')
        config_file_w.write("download_path = " + new_download_path)
        config_file_w.close()
        
    download_path = new_download_path
    global yd
    yd.set_download_path(download_path)
    refresh_label(label, download_path)
    
def refresh_label(label: tk.Label, path: str):
    label.config(text= path)
    
def clear(box: tk.Entry):
    box.delete(0,END)
    
def download(link: str, open_file_confirmation: BooleanVar, download_audio_only_confirmation: BooleanVar):
    if link == "":
        messagebox.showwarning("Error downloading video file", "Provide a link video to download")
    elif "watch" not in link:
        messagebox.showerror("Error downloading video file", "The given video link was not found.")
    else:
        show_download_window(link, open_file_confirmation, download_audio_only_confirmation)
        
def download_video(link: str, open_file_confirmation: bool):
    global yd
    yd.set_url(link)
    yd.get_yt_ob().register_on_progress_callback(show_download_progress)
    yd.get_yt_ob().register_on_complete_callback(show_download_completed)
    yd.download_video(open_file_confirmation)
    
def download_audio(link: str, open_file_confirmation: bool):
    global yd
    yd.set_url(link)
    yd.get_yt_ob().register_on_progress_callback(show_download_progress)
    yd.get_yt_ob().register_on_complete_callback(show_download_completed)
    yd.download_audio(open_file_confirmation)

def show_download_window(link: str, open_file_confirmation: BooleanVar, download_audio_only_confirmation: BooleanVar):
    global file_size
    file_size = 0
    
    global download_window
    download_window = tk.Toplevel()
    download_window.geometry(str(screen_width) + "x" + str(screen_height))
    download_window.attributes("-topmost", True)
    
    download_label = tk.Label(download_window, text= "Downloading...", font=("Sans-serif", 16), justify="center")
    download_label.pack()
        
    global progress_bar    
    progress_bar = Progressbar(download_window, orient= HORIZONTAL, length= 300)
    progress_bar.pack()
        
    global percentage_download
    percentage_download = StringVar()
        
    percentage_download_label = tk.Label(download_window, textvariable= percentage_download)
    percentage_download_label.pack()
        
    global download_complete_label
    download_complete_label = tk.Label(download_window, text= "", font=("Sans-serif", 16), justify="center")
    download_complete_label.pack()
        
    download_window.after(300, lambda: download_process(link, open_file_confirmation, download_audio_only_confirmation))


def download_process(link: str, open_file_confirmation: BooleanVar, download_audio_only_confirmation: BooleanVar):
    if download_audio_only_confirmation.get() is True:
        download_audio(link, open_file_confirmation.get())
    else:
        download_video(link, open_file_confirmation.get())
    
def show_download_progress(stream, chunk: bytes, bytes_remaining: int):
    global file_size
    global download_state
    
    if file_size == 0:
        file_size = bytes_remaining
        download_state = 0
    else:
        download_state = round((file_size - bytes_remaining)*100/file_size, 2)
    
    global progress_bar
    global download_window
    progress_bar['value'] = download_state
    
    global percentage_download
    percentage_download.set(str(download_state) + "%")
    
    print("Downloading...")
    print(percentage_download.get())
    
    
    download_window.update_idletasks()

def show_download_completed(stream, path: str):
    global download_window
    download_window.update_idletasks()
    download_window.bell()
    
    global download_complete_label
    refresh_label(download_complete_label, "Download completed succesfully")
    
    print("\nDownload completed succesfully.\n")

def main():
    """
    Main method for excecution of the code.
    """
    
    #Creating the main window of the app.
    root = tk.Tk()
    
    #title of the app
    title = "Youtube video downloader"
    root.title(title)

    #Setting of the screen width and height of the windows of the app.
    global screen_width
    global screen_height
    screen_width = 400
    screen_height = 350

    #The size of the text box in scale. (It is not stablished in px units)
    download_box_width = 32

    #A boolean var to indicate whether open the file or not.
    open_file_confirmation = BooleanVar()
    
    #A boolean var to indicate whether or not to download the audio only.
    download_audio_only_confirmation = BooleanVar()
    
    #A variable indicating the name of the configurations file to be used for the download.
    global config_file_name
    config_file_name = "config.txt"
    
    #Here we create a YouTube Downloader class object
    global yd
    yd = youtube_downloader.youtube_downloader()

    #Here we assign the download path through the method set_download_path.
    download_path = set_download_path()

    #Then we stablish it to the YouTube object.
    yd.set_download_path(download_path)
        
    #Figure out how to make the image icon work when exporting the program to .exe
    #icon = PhotoImage(file="Icono.png")
    #root.iconphoto(True, icon)
    
    #Here we set the main characteristics of the main window of the app.
    
    #Here we concatenate the screen width and height to create the canvas.
    #Also we set the main window color to white and the border.
    #Finally we block the option to resize the canvas.
    root.geometry(str(screen_width) + "x" + str(screen_height))
    root.config(bg="White", border= "1px solid")
    root.resizable(False, False)

    #The title of the app is stablished and setted to the canvas.
    title_text = tk.Label(root, text=title, font=("Sans-serif", 20))
    title_text.pack() 

    #Here we give the instructions to the user, in order to let them know what to do and the purpose of the app.
    message = tk.Label(root, text="Put the youtube video link\ninto the box below to download it.", font=("Sans-serif", 16), justify="center")
    message.pack(pady = 40)

    #Here we give an entry box for the user. Here they will provide the link of the video they want to download.
    download_box = tk.Entry(root, font='Sans-serif', border=2,width=download_box_width)
    download_box.place(x=center_element_x(screen_width, download_box_width, "un"), y=140)

    #An options button is added in order to let the user set up the app at their own taste.
    options_button = tk.Button(root, font='Sans-serif 10', text="Options", command=lambda: open_options(download_path))
    options_button.place(x=400 - center_element_x(screen_width, download_box_width, "un"), y=140)

    #Sometimes, the user may paste something wrong or something they didn't meant to, so we stablish a clear button to allow the user to clear the box at any time.
    clear_button = tk.Button(root, font='Sans-serif 10', text="Clear", command=lambda: clear(download_box), width=6)
    clear_button.place(x=400 - center_element_x(screen_width, download_box_width, "un"), y=168)

    #Here we set the download button. It's big and it's clear what the button does.
    download_video_button = tk.Button(root,
                                      font='Sans-serif 24',
                                      text="Download",
                                      command= lambda: download(download_box.get(), open_file_confirmation, download_audio_only_confirmation))
    download_video_button.pack()
    
    #We noticed that one of the most common actions the users do is to press the return button in order to let the download begin.
    #Here we stablished the key bind to facilitate the download to the users.
    root.bind("<Return>", lambda event: download(download_box.get(), open_file_confirmation, download_audio_only_confirmation))

    #We put some check buttons in order to let the user take quick actions.
    #This check button allows the app to know whether the user wants to open the file after the download has finished or not.
    check_open_file = tk.Checkbutton(root,
                                    font='Sans-serif 10',
                                    text="Open the file when the download ends",
                                    variable= open_file_confirmation,
                                    onvalue= True,
                                    offvalue= False)
    check_open_file.pack()

    #This check button allows the app to know whether the user wants to download the audio only or not.
    download_audio_only = tk.Checkbutton(root,
                                    font='Sans-serif 10',
                                    text="Download audio only",
                                    variable= download_audio_only_confirmation,
                                    onvalue= True,
                                    offvalue= False)
    download_audio_only.pack()
    
    #This is a label that let's the user know who the author of the application is.
    autor = tk.Label(root, font='Sans-serif 8', text="Author: Alejandro Fonseca Téllez\nAll Rights Reserved")
    autor.pack()

    #Main loop for keeping the app running.
    root.mainloop()

#Protocol setup if
if __name__ == "__main__":
    main()