from bs4 import BeautifulSoup
from os import path
from pathlib import Path
import requests
from sys import argv

BASE_FOLDER = "res/"

def download_images(soup):
    for img in soup.find_all("img"):
        src = img.get("src") # TODO: Use data-src
        if img and src:
            print("Downloading Image: ", src)
            file_path = download_resource("images", src)
            if file_path:
                img["src"] = file_path
                print("Replacing URL with local image:", file_path)


def download_resource(directory, url):
    # Deal with base folder
    if path.exists(BASE_FOLDER) and path.isdir(BASE_FOLDER):
        print("Base folder exists at", BASE_FOLDER)
    else:
        print("Creating base folder:", BASE_FOLDER)
    
    # Check for directory
    directory = path.join(BASE_FOLDER, directory)
    if path.exists(directory) and path.isdir(directory):
        print(directory, "exists")
    else: # Doesn't exist, create
        print("Creating folder:", directory)
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Setup file_name
    file_name = file_name = url.split('/')[-1] # Retrieve filename from URL
    file_name = file_name.split('?')[0] # Remove query string (if applicable)

    dst = path.join(directory, file_name)
    if not path.exists(dst): # Check if destination exists
        with open(dst, "wb") as f:
            res = requests.get(url)
            res.raw.decode_content = True
            f.write(res.content) # Write image to file
    else:
        print("File already exists at", dst, "- skipping")

    return dst


def read_html(file_name="index.html"):
    with open(file_name, "r") as f:
        return f.read()
    return None



def run(html):
    soup = BeautifulSoup(html, "html.parser")
    download_images(soup)
    # TODO: Fonts, Video, etc.

    # Export to file
    with open("offline.html", "w") as f:
        txt = soup.prettify()
        f.write(txt)

html = read_html() # Default read
if len(argv) == 2:
    f = argv[1]
    if path.exists(f) and path.isfile(f):
        print("Using custom file: ", f)
        html = read_html(f)    

if html:
    run(html)
else:
    print("An error occured reading the HTML file")