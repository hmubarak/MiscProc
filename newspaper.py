#http://newspaper.readthedocs.io/en/latest/

from newspaper import Article

import newspaper
newspaper.languages()
####################################

url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
article = Article(url)

######################################
article.download()
article.html

######################################
article.parse()

article.authors
#['Leigh Ann Caldwell', 'John Honway']

article.publish_date
#datetime.datetime(2013, 12, 30, 0, 0)

article.text
#'Washington (CNN) -- Not everyone subscribes to a New Year's resolution...'

article.top_image
#'http://someCDN.com/blah/blah/blah/file.png'

article.movies
#['http://youtube.com/path/to/link.com', ...]

#########################################
article.nlp()

article.keywords
['New Years', 'resolution', ...]

article.summary
'The study shows that 93% of people ...'
#########################################
import newspaper

cnn_paper = newspaper.build('http://cnn.com')

for article in cnn_paper.articles:
    print(article.url)
#http://www.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/
#http://www.cnn.com/2013/12/11/us/texas-teen-dwi-wreck/index.html

for category in cnn_paper.category_urls():
    print(category)

#http://lifestyle.cnn.com
#http://cnn.com/world

cnn_article = cnn_paper.articles[0]
cnn_article.download()
cnn_article.parse()
cnn_article.nlp()
###########################################
from newspaper import fulltext

html = requests.get("cnn.com").text
text = fulltext(html)

##########################################
from newspaper import Article
url = 'http://www.bbc.co.uk/zhongwen/simp/chinese_news/2012/12/121210_hongkong_politics.shtml'

a = Article(url, language='zh') # Chinese

a.download()
a.parse()

print(a.text[:150])
#香港行政长官梁振英在各方压力下就其大宅的违章建

print(a.title)
#港特首梁振英就住宅违建事件道歉
##########################################
import newspaper
sina_paper = newspaper.build('http://www.sina.com.cn/', language='zh')

for category in sina_paper.category_urls():
    print(category)
#http://health.sina.com.cn

article = sina_paper.articles[0]
article.download()
article.parse()

print(article.text)
#新浪武汉汽车综合 随着汽车市场的日趋成熟，

print(article.title)