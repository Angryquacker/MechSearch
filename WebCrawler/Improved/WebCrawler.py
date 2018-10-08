from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import sqlite3
from random import randint
import time

def save(link, keywords):
    vals = [link, keywords]
    conn = sqlite3.connect("links.db")
    db = conn.cursor()
    db.execute("INSERT INTO links VALUES (?, ?)", vals)
    conn.commit()
    conn.close()
    

def crawl(url):
    text = requests.get(url).text
    code = BeautifulSoup(text, "html.parser")
    for link in code.findAll('a'):
        url = link.get("href")
        if url[0:4] != "http":
            break
        else:
            plain = requests.get(url).text
            source = BeautifulSoup(plain, "html.parser")
            for p in source.findAll('p'):
                    keywords = []
                    para = TextBlob(p.text)
                    keywords = keywords + para.noun_phrases
                    save(url, str(keywords))
    nextOne()
    

def nextOne():
    conn = sqlite3.connect('links.db')
    db = conn.cursor()
    db.execute('SELECT link FROM links')
    items = db.fetchall()
    conn.commit()
    conn.close()
    time.sleep(1)
    length = len(items)
    nextLink = str(items[randint(0, length)])
    nextLink = nextLink[:-3][2:]
    crawl(nextLink)

crawl("http://www.cnn.com")
