from bs4 import BeautifulSoup
import webbrowser
import requests

def greater_than(a: int, b: int):
    if a > b:
        return True
    else:
        return False

current_version = "V3.0.4"
current_version = current_version.replace("V","")
separated_digits_current_version = current_version.split(".")

url = "https://github.com/TakNof/YouTube-video-downloader-project/releases"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

latest_version = doc.find_all("span", class_="ml-1 wb-break-all")[0].string.replace("\n","").replace("V","").replace(" ", "")

separated_digits_latest_version = latest_version.split(".")

if any(greater_than(separated_digits_latest_version[i], separated_digits_current_version[i]) for i in range(3)):
    print("There is a newer version of YouTube-video-downloader available. Do you want to download it?")
    if input() == "yes":
        webbrowser.open(url)
else:
    print("The current version of YouTube-video-downloader is up to date.")
    