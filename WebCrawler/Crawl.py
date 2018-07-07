from WebCrawler import spider, valid

url = open('FinalLinks.txt', 'r').readlines()

def st():
    for ur in url:
        spider(ur)

    st()

st()


