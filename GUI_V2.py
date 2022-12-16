from tkinter import END, HORIZONTAL, BooleanVar, PhotoImage, StringVar, filedialog, messagebox
from tkinter.ttk import Progressbar
from bs4 import BeautifulSoup

import os
import youtube_downloader
import tkinter as tk
import cProfile
import time
import webbrowser
import requests

class GUI_V2(tk.Tk):
    def __init__(self, title, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.geometry(f"{str(height)}x{str(width)}")
        self.resizable(False, False)
        
        # The progressbar widget
        self.progressbar = Progressbar(self)
        self.progressbar.pack(fill='x', padx=10)

        # The button widget
        self.button = tk.Button(self, text='Download')
        self.button.pack(padx=10, pady=3, anchor='e')