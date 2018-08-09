import os, io, re, operator
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
import requests

SEARCH_QUERY_INDEX = 0 #0:twitter, 1:facebook, 2:youtube, 3:rss, 4:google+, 5:instagram 6:linkedin
SEARCH_QUERY1 = ["twitter.com",            "facebook.com",            "youtube.com",         "rss/", "plus.google.com",          "instagram.com",           "linkedin.com"]
SEARCH_QUERY2 = ["http://twitter.com/",     "http://facebook.com/",     "http://youtube.com/",  "rss", "http://plus.google.com/",   "http://instagram.com/",    "http://linkedin.com/"]
SEARCH_QUERY3 = ["https://twitter.com/",    "https://facebook.com/",    "https://youtube.com/", "rss", "https://plus.google.com/",  "https://instagram.com/",   "https://linkedin.com/"]

#urls = "D:\\NewsAggregator\\Users\\NewsSources-URLs.txt" # Arabic sources
urls = "D:\\NewsAggregator\\Users\\EnglishSources.txt"  # English sources
#urls = "D:\\NewsAggregator\\Users\\NewsSources-English-Sample100.txt"

TEST_SITE = "" # "http://listverse.com/" #""http://bigthink.com/" #www.news.cn/english/  https://english.alarabiya.net/ http://www.news.cn/english/ http://bigthink.com/
fin = io.open(urls, mode="r", encoding="utf-8")
lines = fin.readlines()

found = 0
with open(urls, mode="r", encoding="utf-8") as fin:
    for cnt, line in enumerate(fin):
        line = line.strip()
        orgLine = line
        #if cnt == 0: # ignore header
        if cnt < 1999:
            continue
        if not line.endswith("/"):
            line += "/"

        if len(TEST_SITE) > 0 and line.find(TEST_SITE) < 0:
            continue

        socialMediaLink = ""
        for trial in range(0, 2):
            try:
                url = line
                if trial > 0:
                    url += "xxx"

                resp = requests.get(url)
                if len(TEST_SITE) > 0:
                    print(resp.text)
                try:
                    resp.text = resp.text.lower()
                except:
                    pass

                soup = BeautifulSoup(resp.text, 'lxml')
                for link in soup.findAll('a'):
                    try:
                        href = link.get('href').strip()
                        if (href.find(SEARCH_QUERY1[SEARCH_QUERY_INDEX]) >= 0) or (href.find(SEARCH_QUERY2[SEARCH_QUERY_INDEX]) >= 0) or (href.find(SEARCH_QUERY3[SEARCH_QUERY_INDEX]) >= 0):
                            socialMediaLink = href
                            break
                    except:
                        pass
            #except Exception as e:
            #    print(e)
            #    socialMediaLink = ""
            except:
                pass

            try:
                if len(socialMediaLink) == 0:
                    for link in soup.findAll('link'):
                        href = link.get('href').strip()
                        if (href.find(SEARCH_QUERY1[SEARCH_QUERY_INDEX]) >= 0) or (href.find(SEARCH_QUERY2[SEARCH_QUERY_INDEX]) >= 0) or (href.find(SEARCH_QUERY3[SEARCH_QUERY_INDEX]) >= 0):
                            socialMediaLink = href
                            break
            except:
                pass

            try:
                if len(socialMediaLink) == 0:
                    for link in soup.findAll('area'):
                        href = link.get('href').strip()
                        if (href.find(SEARCH_QUERY1[SEARCH_QUERY_INDEX]) >= 0) or (href.find(SEARCH_QUERY2[SEARCH_QUERY_INDEX]) >= 0) or (href.find(SEARCH_QUERY3[SEARCH_QUERY_INDEX]) >= 0):
                            socialMediaLink = href
                            break
            except:
                pass

            '''if len(socialMediaLink) > 0 and len(socialMediaLink) < 15:
                if socialMediaLink.endswith("/"):
                    socialMediaLink = line + socialMediaLink
                else:
                    socialMediaLink = line + "/" + socialMediaLink
                socialMediaLink = socialMediaLink.replace("//", "/")
                socialMediaLink = socialMediaLink.replace("/ar/ar/", "/ar/")'''

            if len(socialMediaLink) > 0:
                break

        if len(socialMediaLink) == 0:
            j = start = end = -1
            len2 = len(resp.text)
            j = 0
            while (j >= 0 and j < len2):
                j = resp.text.find(SEARCH_QUERY1[SEARCH_QUERY_INDEX], j + 1)
                if j > 0:
                    for k in range(j - 1, 0, -1):
                        ch = resp.text[k]
                        if ch == '<':
                            start = k
                            break

                    for k in range(j + 1, len2):
                        ch = resp.text[k]
                        if ch == '>':
                            end = k
                            break

                    if (start > -1) and (end > -1):
                        socialMediaLink = resp.text[start:end]

                        if socialMediaLink.startswith("<a "):
                            socialMediaLink2 = ""
                            start2 = socialMediaLink.find('"', 0)
                            if start2 >= 0:
                                end2 = socialMediaLink.find('"', start2 + 1)
                                if end2 > 0:
                                    socialMediaLink2 = socialMediaLink[start2 + 1:end2]

                            if len(socialMediaLink2) > 10:
                                socialMediaLink = socialMediaLink2;
                                break
                            else:
                                socialMediaLink = ""
                        else:
                            socialMediaLink = ""


        if len(socialMediaLink) > 0:
            found += 1
        print("[%d/%d]\t%s\t%s" % (found, cnt, orgLine, socialMediaLink))



