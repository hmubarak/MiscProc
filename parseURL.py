import os, io, re, operator
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer

#urls = "D:\\NewsAggregator\\Users\\NewsSources-URLs.txt"
urls = "D:\\NewsAggregator\\Users\\EnglishSources.txt"

SEARCH_QUERY1 = "www.linkedin.com/" # "www.youtube.com/" "www.facebook.com/" "www.twitter.com/" "rss" "www.plus.google.com" "www.linkedin.com/" "www.instagram.com/" "www.telegram."
SEARCH_QUERY2 = "http://linkedin.com/" # "http://youtube.com/" "http://facebook.com/" "http://twitter.com/" "rss" "http://plus.google.com" "http://linkedin.com/" "http://instagram.com/" "http://telegram."
SEARCH_QUERY3 = "https://linkedin.com/" # "https://youtube.com/" "https://facebook.com/" "https://twitter.com/" "rss" "https://plus.google.com" "https://linkedin.com/" "https://instagram.com/" "https://telegram."

fin = io.open(urls, mode="r", encoding="utf-8")
lines = fin.readlines()

def get_page(url):
    """ loads a webpage into a string """
    src = ""
    req = Request(url)
    try:
        response = urlopen(req)
        CHUNK = 16 * 1024
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            #src += chunk
            src += str(chunk, 'utf-8')
        response.close()
    except IOError:
        print ('can\'t open',url)
        return src

    return src

import requests
from bs4 import BeautifulSoup, SoupStrainer

####################
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

resp = requests.get('https://english.alarabiya.net/x', auth=('Email', 'Pass'), verify=False, cookies={'my': 'cookies'})
txt = resp.text
print(txt)

from bs4 import BeautifulSoup
soup = BeautifulSoup(txt, 'lxml')
for link in soup.findAll('a'):
    href = link.get('href')
    print(href)

######################


with open(urls, mode="r", encoding="utf-8") as fin:
    for cnt, line in enumerate(fin):
        line = line.strip()

        if line.find("https://english.alarabiya.net/") < 0:
            continue

        rss = ""
        try:

            req = Request(line, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()

            #webpage = get_page(line)
            #fin2 = io.open("d:\\tmp\\arb.html", mode="r", encoding="utf-8")
            #webpage = ""
            #for l in fin2.readlines():
            #    webpage += l +" "

            #soup = BeautifulSoup(webpage, 'html.parser', parse_only=SoupStrainer('a', href=True))
            soup = BeautifulSoup(webpage)

            for link in soup.findAll('a'):
                try:
                    href = link.get('href').strip()
                    if (href.find(SEARCH_QUERY1) >= 0) or (href.find(SEARCH_QUERY2) >= 0) or (href.find(SEARCH_QUERY3) >= 0):
                        rss = href
                        #if href.find("http") == 0:
                        #    rss = href
                        #else:
                        #    rss = line + href
                        break
                except:
                    pass
        except Exception as e:
            print(e)
            rss = ""

        try:
            if len(rss) == 0:
                for link in soup.findAll('link'):
                    href = link.get('href').strip()
                    if (href.find(SEARCH_QUERY1) >= 0) or (href.find(SEARCH_QUERY2) >= 0) or (href.find(SEARCH_QUERY3) >= 0):
                        rss = href
                        #if href.find("http") == 0:
                        #    rss = href
                        #else:
                        #    rss = line + href
                        break
        except:
            pass

        if len(rss) > 0 and len(rss) < 15:
            if rss.endswith("/"):
                rss = line + rss
            else:
                rss = line + "/" + rss
            rss = rss.replace("//", "/")
            rss = rss.replace("/ar/ar/", "/ar/")

        print(line + "\t" + rss)


