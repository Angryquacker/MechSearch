import requests
from bs4 import BeautifulSoup


def spider(url):
    file = open('Test.txt', 'r+')
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('a'):
        href = link.get('href')
        file.write(str(href) + '\n')
    file.close()
    valid()

def valid():
    final = open('FinalLinks.txt', 'a')
    file = open('Test.txt', 'r')
    
    for link in file.readlines():
        if link[0] == 'h':
            final.write(link)

    file.close()
    final.close()
