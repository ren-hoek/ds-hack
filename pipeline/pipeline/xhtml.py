from bs4 import BeautifulSoup
import re

def extract_xhtml(xhtml):

    soup = BeautifulSoup(open(xhtml), 'html.parser')

    for tag in soup(["script", "style"]):
        tag.extract()

    text = re.sub('<[^<]+>', " ",str(soup))
    text = text.replace("\n", " ")
    text = re.sub(r'[\W_]+', ' ', text)
    text = text.split(" ")

    return text


def create_text(f):
    xhtml_text = dict()
    xhtml_text['extracted_html'] = extract_xhtml(f)
    return xhtml_text



