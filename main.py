from bs4 import BeautifulSoup

def read_html(file_name="index.html"):
    with open(file_name, "r") as f:
        return f.read()
    return None

html = read_html()
soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())
