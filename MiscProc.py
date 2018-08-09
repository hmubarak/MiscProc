import gzip
import io
from secrets import randbelow

#f=gzip.open("D:\Tweets\Tweets\tweets.2018-01-01.txt.gz",'rb')
#file_content=f.read()
#print file_content

MAX_NOF_TWEETS = 1000000
MAX_NOF_HASHTAGS = 1000
MAX_NOF_CONTEXTS = 10
hashtagFreq = {}

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


infile = io.open("E:/Speech/WAWCorpus/en/test/analysis/GoogleASR.txt", mode="rt", encoding="utf-8")
lines = infile.readlines()
for line in lines:
    if line.startswith("Transcript: "):
        line = line.replace("Transcript: ", "")
        line = line.replace("\n", "")
        line = line.strip()
        line = line.lower()
        line = cleanString(line, False, True)
        print(line)
infile.close()



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

def cleanString(s):
    if type(s) is str:
        if (not s) or (s is ''):
            empty = True
        else:
            s = s.replace("\r\n", ".")
            s = s.replace("\r", ".")
            s = s.replace("\n", ".")
            s = s.replace("\t", " ")
            s = s.strip()
    if s is None:
        s = ""
    return s

#f=gzip.open("D:\\Tweets\\Tweets\\tweets.2018-01-01.txt.gz", "rt", encoding="UTF8")
#file_content=f.read()
#print (file_content)

nofTweets = 0
errors = 0
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
    tweet.text = str[15];
    tweet.hashTagList = str[18];

    if (nofTweets % 1000) == 0:
        print("[1/2] nofTweets:%d, errors:%d tweet:%s" % (nofTweets, errors, tweet.text))

    if tweet.hashTagList == 'null':
        continue
    hashtags = tweet.hashTagList.split(",")
    for hashtag in hashtags:
        if not hashtag in hashtagFreq:
            freq = 1
        else:
            freq = hashtagFreq[hashtag] + 1
        hashtagFreq[hashtag] = freq
fin.close()

fout = open("D:\\Tweets\\Tweets\\topHashtags1000.txt", "wt", encoding="UTF8")

orgHashtagFreq = hashtagFreq
hashtagFreq = sorted(hashtagFreq.items(), key=lambda t: t[1], reverse=True)
nofHashtags = 0
finalHashtagFreq = {}
for k, v in hashtagFreq:
    out = "%s\t%d\n" % (k, v)
    fout.write(out)
    finalHashtagFreq[k] = 0

    nofHashtags += 1
    if nofHashtags >= MAX_NOF_HASHTAGS:
        break

fout.close()

nofTweets = 0
errors = 0
fin = gzip.open("D:\\Tweets\\Tweets\\tweets.2016-01-01.txt.gz", "rt", encoding="UTF8")
hashtagContexts = {}
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
    tweet.hashTagList = str[18];

    if (nofTweets % 1000) == 0:
        print("[2/2] nofTweets:%d, errors:%d tweet:%s" % (nofTweets, errors, tweet.text))

    if tweet.hashTagList == 'null':
        continue
    hashtags = tweet.hashTagList.split(",")
    for hashtag in hashtags:
        if hashtag in finalHashtagFreq:
            r = randbelow(10) # take random contexts
            if r == 5:
                freq = finalHashtagFreq[hashtag] + 1
                finalHashtagFreq[hashtag] = freq

                if freq <= MAX_NOF_CONTEXTS:
                    tweet.text = cleanString(tweet.text)
                    out = "%d\t%s" % (tweet.tweetId, tweet.text)
                    if hashtag in hashtagContexts:
                        out2 = hashtagContexts[hashtag]
                        out = "%s\t%s" % (out2, out)
                        hashtagContexts[hashtag] = out
                    else:
                        hashtagContexts[hashtag] = out

fout = open("D:\\Tweets\\Tweets\\topHashtags1000Contexts.txt", "wt", encoding="UTF8")
for k2, v2 in hashtagContexts.items():
    freq = orgHashtagFreq[k2]
    out = "%s\t%d\t%s\n" % (k2, freq, v2)
    fout.write(out)

fin.close()
fout.close()
