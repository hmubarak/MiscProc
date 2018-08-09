import gzip
from secrets import randbelow

#f=gzip.open("D:\Tweets\Tweets\tweets.2018-01-01.txt.gz",'rb')
#file_content=f.read()
#print file_content

MAX_NOF_TWEETS = -1
MAX_NOF_HASHTAGS = 1000
MAX_NOF_CONTEXTS = 10

'''
    tweet.tweetId = fields[0];
    tweet.fromUserId = fields[1];
    tweet.fromUserName = fields[2];
    tweet.fromUserScreenName = fields[3];
    tweet.fromUserBigProfileImageURL = fields[4];
    tweet.fromUserTimeZone = fields[5];
    tweet.fromUserFollowersCount = fields[6];
    tweet.fromUserFolloweesCount = fields[7];
    tweet.fromUserLocation = fields[8];
    tweet.fromUserLang = fields[9];
    tweet.source = fields[10];
    tweet.country = fields[11];
    tweet.place = fields[12];
    tweet.coordinates = fields[13];
    tweet.createdAt = fields[14];
    tweet.text = fields[15];
    tweet.URLList = fields[16];
    tweet.mediaURLList = fields[17];
    tweet.hashTagList = fields[18];
    tweet.mentionsList = fields[19];
    tweet.retweetCount = fields[20];
    tweet.originalTweetId = fields[21];
    tweet.originalTweetText = fields[22];
'''

class TweetInfo(object):
    #def __init__(a, b):
    #    self.a = a
    #    self.b = b
    tweetId = fromUserId = 0
    fromUserName = fromUserScreenName = fromUserBigProfileImageURL = fromUserTimeZone = ""
    fromUserFollowersCount = fromUserFolloweesCount = 0
    fromUserLocation = fromUserLang = source = country = place = coordinates = createdAt = text = URLList = mediaURLList = hashTagList = mentionsList = ""
    retweetCount = 0
    originalTweetId = originalTweetText = ""

def cleanString(s, normalize, cleanPunc):
    if type(s) is str:
        if (not s) or (s is ''):
            empty = True
        else:
            s = s.replace("\r\n", ".")
            s = s.replace("\r", ".")
            s = s.replace("\n", ".")
            s = s.replace("\t", " ")

            if normalize:
                s = s.replace("أ", "ا")
                s = s.replace("إ", "ا")
                s = s.replace("آ", "ا")
                s = s.replace("ة", "ه")
                s = s.replace("ى", "ي")
            if cleanPunc:
                s = s.replace("_", " ")
                s = s.replace("-", " ")
                s = s.replace("#", " ")
                s = s.replace(".", " ")
                s = s.replace(",", " ")

            s = s.replace("  ", " ")
            s = s.strip()


    if s is None:
        s = ""
    return s

#f=gzip.open("D:\\Tweets\\Tweets\\tweets.2018-01-01.txt.gz", "rt", encoding="UTF8")
#file_content=f.read()
#print (file_content)

f = open("D:\\NewsAggregator\\controversialTopics2.txt", "rt", encoding="UTF8")
controvTopics = f.read()
controvTopics = controvTopics.split("\n")
for i in range(0, len(controvTopics)):
    controvTopics[i] = " %s " % controvTopics[i]
f.close

fout = open("D:\\Tweets\\Tweets\\controversialTopics2Tweets.txt", "wt", encoding="UTF8")

nofTweets = 0
errors = 0
found = 0
fin = gzip.open("D:\\Tweets\\Tweets\\tweets.2016-01-01.txt.gz", "rt", encoding="UTF8")
for line in fin:
    nofTweets += 1
    if nofTweets == MAX_NOF_TWEETS:
        break

    str = line.split("\t")
    if len(str) != 23:
        errors += 1
        continue;

    tweet = TweetInfo()
    tweet.tweetId = int(str[0])
    tweet.text = str[15];
    tweet.text = cleanString(tweet.text, False, False)

    if (nofTweets % 1000) == 0:
        print("[1/2] nofTweets:%d, errors:%d found:%d tweet:%s" % (nofTweets, errors, found, tweet.text))

    text = cleanString(tweet.text, True, True)
    text = " %s " % (text)
    for w in controvTopics:
        if text.find(w) >= 0:
            out = "%s\t%d\t%s\n" % (w, tweet.tweetId, tweet.text)
            fout.write(out)
            found += 1
            break;

fin.close()
