from bs4 import BeautifulSoup
from os import path
from pathlib import Path
import requests
import mimetypes

BASE_FOLDER = "res/"

def download_images(soup):
    for img in soup.find_all("img"):
        src = img.get("src")
        if img and src:
            print("Downloading Image: ", src)
            # img["src"] = "new url"
            download_resource("images", src)


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

    # Download resource
    res = requests.get(url)
    file_name = file_name = url.split('/')[-1] # Retrieve filename from URL
    file_name = file_name.split('?')[0] # Remove query string (if applicable)

    # mimetypes.init()
    # file_type = mimetypes.guess_type(url)
    # file_type = mimetypes.guess_extension(file_type)
    # print(file_name, file_type)

    dst = path.join(directory, file_name)
    if not path.exists(dst): # Check if destination exists
        with open(dst, "wb") as f:
            res.raw.decode_content = True
            f.write(res.content) # Write image to file
            return file_name
    else:
        print("File already exists at", dst, "- skipping")

    return None


def read_html(file_name="index.html"):
    with open(file_name, "r") as f:
        return f.read()
    return None



def run(html):
    soup = BeautifulSoup(html, "html.parser")
    download_images(soup)


html = read_html()
if html:
    run(html)
else:
    print("An error occured reading the HTML file")