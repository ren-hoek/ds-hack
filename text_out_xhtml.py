import re
from bs4 import BeautifulSoup

page = ""

soup = BeautifulSoup((open(page)), 'html.parser')

for script in soup(["script", "style"]):
        script.extract()

text = re.sub('<[^<]+>', "", str(soup))
