from bs4 import BeautifulSoup

def read_html(file_name="index.html"):
    with open(file_name, "r") as f:
        return f.read()
    return None


def run(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())


html = read_html()
if html:
    run(html)
else:
    print("An error occured reading the HTML file")