import os

if(os.path.exists("config.txt") is False):
    with open("config.txt", "w") as config_file:
        config_file.write("download_path = None")
        config_file.close()
