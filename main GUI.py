from tkinter import END, HORIZONTAL, BooleanVar, PhotoImage, StringVar, filedialog, messagebox
from tkinter.ttk import Progressbar

import os
import youtube_downloader
import tkinter as tk
import cProfile
import time

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
    download_path_message = tk.Label(options_window, text=f"The current download folder is:\n{download_path}", font=("consolas", 14), justify="left")
    download_path_message.pack(padx=0)
    
    #Here we set a button to let the user change the download path as they wish.
    change_download_path_button = tk.Button(options_window,
                                            text="Change the download path",
                                            cursor="hand2",
                                            activebackground="#badee2",
                                            command = lambda: change_download_path(download_path_message),
                                            font=("Consolas", 12))
    change_download_path_button.pack(padx=0)
    
    #Here we set a button to let the user open the folder were the download path was set.
    open_selected_folder_button = tk.Button(options_window,
                                    text= "Open selected folder",
                                    cursor="hand2",
                                    activebackground="#badee2",
                                    command= lambda: open_selected_folder(),
                                    font=("Consolas", 12))
    open_selected_folder_button.pack(padx=0)
    
    #Here we set a button to let the user open the folder were the download path was set.
    reset_download_path_button = tk.Button(options_window,
                                    text= "Reset download path",
                                    cursor="hand2",
                                    activebackground="#badee2",
                                    command= lambda: set_download_path_to_default(download_path_message),
                                    font=("Consolas", 12))
    reset_download_path_button.pack(padx=0)
    
def open_selected_folder():
    """
    This method allows to open selected folder where the files will be downloaded.
    """
    os.startfile(set_download_path())
    
def set_download_path_to_default(label: tk.Label):
    """
    
    Args:
        options_window (tk.Toplevel): _description_
        label (tk.Label): _description_
    """
    #Here we set the download path to its default value.
    download_path = default_download_path
    
    #We give it as well to the class.
    yd.set_download_path(download_path)
    
    #Refresh the label through the method.
    refresh_label(label, f"The current download folder is:\n{download_path}")

    #And finally we rewrite its value in the config.txt file.
    config_file_w = open(config_file_name, 'w')
    config_file_w.write("download_path = " + default_download_path)
    config_file_w.close()
      
def set_download_path():
    """
    This method sets the path where the files will be downloaded.
    Returns:
        str: The download path as a string.
    """
    
    #Here we check if the txt file with the download path exists to load the preseted download path to the program through the method.
    #In case an error is encountered, there is created a file with the preseted name and the preseted download path to the default download
    #folder of th user in the windows OS.  
    try:
        config_file_r = open(config_file_name, 'r')
        read_config_file = config_file_r.readline()
        config_file_r.close()
        
        #Through this conditional we check if the download path or the file itself
        #is empty, if so we raise an exception to stablish the path, otherwise it preceeds normaly.
        if read_config_file == "" or read_config_file.split("=")[-1] == "":
            raise IOError("Download path is empty.")
        else:
            return read_config_file.split("= ")[-1]
    except IOError:
        config_file_w = open(config_file_name, 'w')
        config_file_w.write("download_path = " + default_download_path)
        
        return default_download_path   

def change_download_path(label: tk.Label):
    """
    This method allows the user to change the download path as they wish.
    Args:
        label (tk.Label): An object representing a label of tkinter.
    """
    #This option allows the user to select the folder where he wants to download the file in a user-friendly manner
    #using the windows OS default tab to do it. A big advantage of this approach is that we do not have to manually
    #stablish the errors on the selection of the folder.
    new_download_path = filedialog.askdirectory()

    #Here we load the choosen folder path to the download path variable, if not empty.
    if new_download_path != "":
        config_file_w = open(config_file_name, 'w')
        config_file_w.write("download_path = " + new_download_path)
        config_file_w.close()
        
        download_path = new_download_path
        #Same happens for the youtube object of the youtube_downloader class.
        yd.set_download_path(download_path)
        #Finally, we refresh the label through the created method.
        refresh_label(label, f"The current download folder is:\n{download_path}")
    
def refresh_label(label: tk.Label, new_str: str):
    """
    This method allows you to refresh the label.
    Args:
        label (tk.Label): An object representing a label of tkinter.
        new_str (str): The new string which will be dislplayed in the label.
    """
    label.config(text= new_str)
    
def clear(box: tk.Entry):
    """
    This method clears the link box of the application.
    Args:
        box (tk.Entry): An object representing a box of tkinter
    """
    box.delete(0,END)
    
def download(link: str, open_file_confirmation: BooleanVar, download_audio_only_confirmation: BooleanVar):
    """
    This method downloads the video or audio file from the specified link given.
    Args:
        link (str): The link of the video or playlist to be downloaded.
        open_file_confirmation (BooleanVar): The boolean flag to indicate whether to open the file or not when downloaded.
        download_audio_only_confirmation (BooleanVar): The boolean flag to indicate whether to download only the audio oh the video or not.
    """
    #If an error is encountered this conditional will show the user the specific cause of the error, 
    #as well as stoping the process in order to prevent a crash of the application.
    #Otherwise the download screen will be displayed indicating that the download has begun successfully.
    if link == "":
        messagebox.showwarning("Error downloading video file", "Provide a link video to download")
    elif "watch" not in link and "playlist" not in link:
        messagebox.showerror("Error downloading video file", "The given video link was not found.")
    else:
        #Here we have to check whether the url corresponds to a video or a playlist, so we check it using the
        #keywords located in the url itself. This changes some of the processes of previous versions.
        if "playlist" in link or "list" in link:
            global is_playlist
            is_playlist = True
        show_download_window(link, open_file_confirmation, download_audio_only_confirmation)
        
def show_download_window(link: str, open_file_confirmation: BooleanVar, download_audio_only_confirmation: BooleanVar):
    """
    This method dislplays the download window.
    Args:
        link (str): The link of the video or playlist to be downloaded.
        open_file_confirmation (BooleanVar): The boolean flag to indicate whether to open the file or not when downloaded.
        download_audio_only_confirmation (BooleanVar): The boolean flag to indicate whether to download only the audio oh the video or not.
    """
    #The file we will be downloading has its own size in bytes, so we need to create a variable to collect it, in order to display it
    #to the user indicating the time remainning of the download to finish.    
    global download_window
    download_window = tk.Toplevel()
    download_window.geometry(str(screen_width) + "x" + str(screen_height))
    download_window.attributes("-topmost", True)
    
    #Here we stablish the atributes of the window.
    
    #The main label.
    download_label = tk.Label(download_window, text= "Downloading...", font=("Sans-serif", 16), justify="center")
    download_label.pack()
    
    #The main progress bar.
    global main_progress_bar    
    main_progress_bar = Progressbar(download_window, orient= HORIZONTAL, length= 300)
    main_progress_bar.pack()
    
    #The percentage of progress of the download.
    global percentage_download
    #Owing to the fact that the percentage of progress has to change through time it has to be stablished in this way.
    percentage_download = StringVar()
    percentage_download.set("Starting download...") 
    percentage_download_label = tk.Label(download_window, textvariable= percentage_download)
    percentage_download_label.pack()
    
    #The bytes downloaded.
    global bytes_downloaded
    #Owing to the fact that the bytes downloaded changes through time it has to be stablished in this way.
    bytes_downloaded = StringVar()
    bytes_downloaded_label = tk.Label(download_window, textvariable= bytes_downloaded)
    bytes_downloaded_label.pack()
    
    #The following items should be displayed only if the url given is a playlist.
    if is_playlist:
        #The task progress bar in case of donwloading a playlist.
        global task_progress_bar    
        task_progress_bar = Progressbar(download_window, orient= HORIZONTAL, length= 300)
        task_progress_bar.pack()
            
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
    
    #It necessary to give the app certain time to display its elements before starting the download, 
    #so that why we use this function to call the download process method with a delay of 500ms.
    download_window.after(500, lambda: download_process(link, open_file_confirmation.get(), download_audio_only_confirmation.get()))

def download_process(link: str, open_file_confirmation: bool, download_audio_only_confirmation: bool):
    """
    This method starts the download process.
    Args:
        link (str): The link of the video or playlist to be downloaded.
        open_file_confirmation (BooleanVar): The boolean flag to indicate whether to open the file or not when downloaded.
        download_audio_only_confirmation (BooleanVar): The boolean flag to indicate whether to download only the audio oh the video or not.
    """
    global is_playlist
    #Here we load the link of the video or playlist to the class.
    yd.set_url(link)
    
    #Boolean flag to take one process or another.
    if is_playlist:
        
        #If true, then it means there are multiple downloads to be done. So we have to check how many elements
        #are going to be downloaded. We create a global variable and we use the playlist object to do it so.
        global total_tasks
        total_tasks = len(yd.get_pl_ob().video_urls)
        
        #As well, we need to let the user know how many elements have been downloaded since the start of the process.
        #So we need a count of the current number of elements that have been downloaded successfully.
        global current_task
        current_task = 0
        
        #In order to show the amount of data that will be downloaded, we need to collect all the size of the
        #files to be downloaded. We do this by iterating over a for loop.
        global total_size_of_download
        total_size_of_download = 0
        for video in yd.get_pl_ob().video_urls:
            total_size_of_download += int(yd.get_size_of_file(download_audio_only_confirmation, True, video))

        #This variable collects the current state of the total donwload.
        global current_total_download
        current_total_download = 0

        #This variable collects the specified size of the current iterated video.
        global specific_file_size_of_download
        specific_file_size_of_download = 0
               
        #A for cicle to iterate along all the video urls in the playlist.
        for video in yd.get_pl_ob().video_urls:
            #We set the file size as global and stablish it as 0 for each time the loop is executed.
            global file_size
            file_size = 0
            
            #Here we create the YouTube object through the modified method.
            yd.set_yt_ob(True, video)
            yd.set_download_file_name()
            
            #We stabilish its value through the method.
            specific_file_size_of_download = yd.get_size_of_file(download_audio_only_confirmation, True, video)                               
           
            #We use the methods to register the progress and the completion of the download.
            yd.get_yt_ob().register_on_progress_callback(show_main_download_progress)
            yd.get_yt_ob().register_on_complete_callback(show_main_download_completed)
                       
            #Conditional to know if whether the video or the audio is going to be downloaded.
            if download_audio_only_confirmation is True:
                yd.download_audio(open_file_confirmation)
            else: 
                yd.download_video(open_file_confirmation)
            
            #We stablish this variable at the end of the loop because we know for sure that
            #the current state of the total donwload corresponds to the sum of all the specific ones
            #at the end of each iteration.
            current_total_download += specific_file_size_of_download
            specific_file_size_of_download = 0  
        #Here we reset this variables for future uses.
        current_task = 0
        current_total_download = 0       
        
    else:
        #This variable collects the total file size of the video.
        specific_file_size_of_download = yd.get_size_of_file(download_audio_only_confirmation)
        
        #We use the methods to register the progress and the completion of the download.
        yd.get_yt_ob().register_on_progress_callback(show_main_download_progress)
        yd.get_yt_ob().register_on_complete_callback(show_main_download_completed)
        
        #Conditional to know if whether the video or the audio is going to be downloaded.
        if download_audio_only_confirmation is True:
            yd.download_audio(open_file_confirmation)
        else: 
            yd.download_video(open_file_confirmation)
    
def show_main_download_progress(stream, chunk: bytes, bytes_remaining: int):
    """
    This method shows the progress of the download.
    Args:
        stream (_type_): The stream of the video to download.
        chunk (bytes): Amount of bytes to download.
        bytes_remaining (int): The bytes remaining to download.
    """   
    #First here we set that if the variable file size is empty means that it has not storaged
    #the real file size, therefore we know that the bytes remaining will be the real file size.
    #Here we stablish the download state variable too.
    #When the file size is determined we start loading the values of the download state to its
    #variable, calculating it through a simply procedure.
    global file_size
    if file_size == 0:
        file_size = bytes_remaining
        download_state = 0
    else:
        download_state = str(round((file_size - bytes_remaining)*100/file_size, 2))
        
    #The variable of the progress bar is determined by the download state variable.
    global main_progress_bar  
    main_progress_bar['value'] = download_state
    
    #So does the percentage of the download.
    global percentage_download
    percentage_download.set(str(download_state) + "%")
    
    #This variable collects the progress of the download in its corresponding unit of storage.
    global bytes_downloaded
    bytes_downloaded.set(
        "".join([str(item) for item in convert_bytes(round(specific_file_size_of_download - int(bytes_remaining), 2))]) 
        + "/" + 
        "".join([str(item) for item in convert_bytes(round(specific_file_size_of_download, 2))]))
    
    #A conditional to display the progress bar of the individual tasks.
    if is_playlist:
        #This variable collects the progress of the download in its corresponding unit of storage.
        global total_bytes_downloaded
        total_bytes_downloaded.set(
            "".join([str(item) for item in convert_bytes(round(current_total_download + specific_file_size_of_download - int(bytes_remaining), 2))]) 
            + "/" + 
            "".join([str(item) for item in convert_bytes(round(total_size_of_download, 2))]))
    
        
        #A conditional to display the label of the specific task progress.
        if bytes_remaining == 0:
            global current_task
            current_task += 1
        
        #Due it is a playlist, we need to display the progress for each item and in general.
        show_task_progress()
   
    #Lastly, we update the labels every time a cycle of the callback is executed.
    global download_window
    download_window.update_idletasks()

def show_main_download_completed(stream, path: str):
    """
    This method shows the completion of the download in the window.
    Args:
        stream (_type_): The stream of the video to download.
        path(str): The path to the video to download.
    """
            
    #The label shows finally the message.
    global download_complete_label
    if is_playlist:
        if current_task == total_tasks:
            refresh_label(download_complete_label, "Download completed succesfully")
    else:
        refresh_label(download_complete_label, "Download completed succesfully")
    
    #When the download is completed, we update the windows one more time to show it to the user.
    #Then a bell sounds, indicating the completion of the download.
    global download_window
    download_window.update_idletasks()
    download_window.bell()

def show_task_progress():
    """
    This method shows the progress of the tasks downloading.
    """
    #Now this task progress is determined by the amount of tasks completed and the total number of tasks to finish.
    global current_task
    global total_tasks
    task_state = str((current_task/total_tasks)*100)
    
    #The variable of the progress var is determined by the task state variable.
    global task_progress_bar
    task_progress_bar['value'] = task_state
        
    #So does the percentage of the download.
    global tasks_completed
    tasks_completed.set(str(current_task) + "/" + str(total_tasks) + " videos downloaded.")    

def convert_bytes(bytes_given: int) -> list:
    """
    This method converts the bytes given to a more human-readable representation.
    Args:
        bytes_given (int): The amount of bytes to convert.

    Returns:
        list: [units converted, kind of unit]
    """
    if bytes_given/1024 <= 100:
        return [round(bytes_given/1024, 2), "KB"]
    elif bytes_given/1048576 <= 1000:
        return [round(bytes_given/1048576, 2), "MB"]
    elif bytes_given/10737418274 <= 10:
        return [round(bytes_given/1073741824, 2), "GB"]
    elif bytes_given/1099511627776 <= 10:
        return [round(bytes_given/1099511627776, 2), "TB"]     

def main():
    """
    Main method for excecution of the code.
    """
    #Indicates the current version of the application
    app_version_text = "V3.1.0"
    
    #Creating the main window of the app.
    root = tk.Tk()
    
    #title of the app
    title = "YouTube video downloader \n" + app_version_text
    root.title(title)

    #Setting of the screen width and height of the windows of the app.
    global screen_width
    global screen_height
    screen_width = 400
    screen_height = 400

    #Letter types.
    letter_type1 = 'Sans-serif 10'
    letter_type2 = 'Sans-serif 8'
    
    #The size of the text box in scale. (It is not stablished in px units)
    download_box_width = 32

    #A boolean var to indicate whether open the file or not.
    open_file_confirmation = BooleanVar()
    
    #A boolean var to indicate whether or not to download the audio only.
    download_audio_only_confirmation = BooleanVar()
    
    #A variable indicating the name of the configurations file to be used for the download.
    global config_file_name
    config_file_name = "config.txt"
    
    #A variable indicating the default download path of the windows OS users.
    global default_download_path
    default_download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))
    
    #Here we create a YouTube Downloader class object
    global yd
    yd = youtube_downloader.youtube_downloader()
    
    #The file to be downloaded will have its file size, so we create a variable to save it.
    global file_size
    file_size = 0
    
    #As well, when downloading it will have a current state of download, so we save it in a variable.
    global download_state
    download_state = 0

    #Here we assign the download path through the method set_download_path.
    global download_path
    download_path = set_download_path()
    
    #If the link provided is a playlist we state a boolean variable to indicate whether it is or not.
    global is_playlist
    is_playlist = False

    #Then we stablish it to the YouTube object.
    yd.set_download_path(download_path)
        
    #Here the icon of the application is loaded.
    icon = PhotoImage(file="Icono.png")
    root.iconphoto(True, icon)
    
    #Here we set the main characteristics of the main window of the app.
    
    #Here we concatenate the screen width and height to create the canvas.
    #Also we set the main window color to white and the border.
    #Finally we block the option to resize the canvas.
    root.geometry(str(screen_width) + "x" + str(screen_height))
    root.config(bg="White", border= "1px solid")
    root.resizable(False, False)

    #Here we center the left-upper corner of the aplication window.
    root.eval("tk::PlaceWindow . center")
    
    #The title of the app is stablished and setted to the canvas.
    title_text = tk.Label(root, text=title, font=("Sans-serif", 20))
    title_text.pack() 

    #Here we give the instructions to the user, in order to let them know what to do and the purpose of the app.
    message = tk.Label(root, text="Put the youtube video or playlist link\ninto the box below to download it.", font=("Sans-serif", 16), justify="center")
    message.pack(pady = 10)

    #Here we give an entry box for the user. Here they will provide the link of the video or playlist they want to download.
    download_box = tk.Entry(root, font='Sans-serif', border=2,width=download_box_width)
    download_box.place(x=center_element_x(screen_width, download_box_width, "un"), y=140)

    #An options button is added in order to let the user set up the app at their own taste.
    options_button = tk.Button(root,
                               font=letter_type1,
                               text="Options",
                               cursor="hand2",
                               activebackground="#badee2",
                               command=lambda: open_options(download_path))
    options_button.place(x=400 - center_element_x(screen_width, download_box_width, "un"), y=140)

    #Sometimes, the user may paste something wrong or something they didn't meant to, so we stablish a clear button to allow the user to clear the box at any time.
    clear_button = tk.Button(root,
                             font=letter_type1,
                             text="Clear",
                             cursor="hand2",
                             command=lambda: clear(download_box), width=6)
    clear_button.place(x=400 - center_element_x(screen_width, download_box_width, "un"), y=168)

    #Here we set the download button. It's big and it's clear what the button does.
    download_button = tk.Button(root,
                                    font='Sans-serif 24',
                                    text="Download",
                                    cursor="hand2",
                                    activebackground="#badee2",
                                    command= lambda: download(download_box.get(), open_file_confirmation, download_audio_only_confirmation)
                                    )
    download_button.pack(pady = 30)
    
    #We noticed that one of the most common actions the users do is to press the return button in order to let the download begin.
    #Here we stablished the key bind to facilitate the download to the users.
    root.bind("<Return>", lambda event: download(download_box.get(), open_file_confirmation, download_audio_only_confirmation))

    #We put some check buttons in order to let the user take quick actions.
    #This check button allows the app to know whether the user wants to open the file after the download has finished or not.
    check_open_file = tk.Checkbutton(root,
                                    font=letter_type1,
                                    text="Open the file when the download ends",
                                    cursor="hand2",
                                    activebackground="#badee2",
                                    variable= open_file_confirmation,
                                    onvalue= True,
                                    offvalue= False)
    check_open_file.pack()

    #This check button allows the app to know whether the user wants to download the audio only or not.
    download_audio_only = tk.Checkbutton(root,
                                    font=letter_type1,
                                    text="Download audio only",
                                    cursor="hand2",
                                    activebackground="#badee2",
                                    variable= download_audio_only_confirmation,
                                    onvalue= True,
                                    offvalue= False)
    download_audio_only.pack()
    
    #This is a label that let's the user know who the author of the application is.
    autor = tk.Label(root, font=letter_type2, text="Author: Alejandro Fonseca Téllez\nAll Rights Reserved")
    autor.pack()
    
    #This is a label that let's the user know what is the application version they are using.
    app_version = tk.Label(root, font=letter_type2, text= app_version_text)
    app_version.pack()

    #Main loop for keeping the app running.
    root.mainloop()

#Protocol setup if
if __name__ == "__main__":
    main()
    #cProfile.run('main()', sort='tottime')
    #print(time.perf_counter())