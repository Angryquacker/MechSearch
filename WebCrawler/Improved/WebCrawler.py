from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import sqlite3
from random import randint
import gc
import time


def save(link, keywords):
    val = [link, keywords]
    db.execute("INSERT INTO links VALUES (?, ?)", val)
    conn.commit()


def crawl(url):
    global counts
    global conn
    global db
    if counts == -1:
        conn = sqlite3.connect('links.db')
        db = conn.cursor()
        counts = 0
    elif counts == 1000:
        conn.commit()
        conn.close()
        conn = sqlite3.connect('links.db')
        db = conn.cursor()
        counts = 0
    else:
        counts = counts + 1
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
    next_one()


def next_one():
    db.execute('SELECT link FROM links')
    items = db.fetchall()
    conn.commit()
    length = len(items)
    next_link = str(items[randint(0, length)])
    next_link = next_link[:-3][2:]
    crawl(next_link)


counts = -1
crawl("http://www.youtube.com")