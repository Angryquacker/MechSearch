from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import mysql.connector
from random import randint
import time


def save(link, keywords):
    val = [link, keywords]
    db.execute("INSERT INTO links(link, keywords) VALUES (%s, %s)", val)
    cnx.commit()


def crawl(url):
    global cnx
    global db
    if count == -1:
        cnx = mysql.connector.connect(user='#', password='#', host='#', database='links')
        db = cnx.cursor()
        count = 0
    elif count == 1000:
        cnx.close()
        db.close()
        time.sleep(1)
        cnx = mysql.connector.connect(user='#', password='#', host='#', database='links')
        db = cnx.cursor()
        time.sleep(1)
    else:
        count = count + 1
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
    db.execute('SELECT * FROM links')
    items = db.fetchall()
    length = db.rowcount
    next_link = items[randint(0, length - 1)]
    next_link = next_link[1]
    crawl(next_link)

global count
count = -1
crawl("http://www.youtube.com")
