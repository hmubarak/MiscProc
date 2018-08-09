#!/usr/bin/python

## Simple adapter that reads a file with text, and translates each
# line using our MT backend. The script can handle files where each
# line is preceeded by a marker such as an index (using the -m flag)
#
# <marker> <text>
# <marker> <text>
#
# The language pair is given using the -l flag. If no input/output
# files are provided, stdin/stdout are assumed respectively.
#
# Author: Fahim Dalvi

MY_KEY = "44045472498880a4e491c12ec6db76c4"

import argparse
import codecs
import os
import requests
import urllib
import sys
import io
import re

BASE_URL = "https://mt.qcri.org/api/v1/"

LANG_PAIRS = "en-ar"
MT_SYSTEM = "general" #"general", "neural-opus-dev"

inFoldername = "E:/Speech/WAWCorpus/en/test"

# Help Strings
PROG_DESCRIPTION = "Translate each line from the input file from arabic to english"
INPUT_HELP = "Path to the input file | Default: stdin"
OUTPUT_HELP = "Path to the output file | Default: stdout"
SERVER_HELP = "Server URL where the MT API is hosted"
API_HELP = "API key to use for the rest services"
MARKER_HELP = "Flag to indicate if each line starts with a marker"
LANG_HELP = "Language pair to use. `en-ar` and `ar-en` supported."
DOMAIN_HELP = "Domain to select appropriate translation model."
VERBOSE_HELP = "Print progress and first few characters every 10 requests"
SKIP_HELP = "Skip the first n lines in the source file"

SILENCE_BETWEEN_WORDS = 0.5

def normalizeString(s):
    s = s.replace("أ", "ا")
    s = s.replace("إ", "ا")
    s = s.replace("آ", "ا")

    # remove diac
    s = re.sub("َ|ُ|ِ|ً|ٌ|ٍ|ّ|ْ", "", s)
    return s


def parse_args():
    parser = argparse.ArgumentParser(description=PROG_DESCRIPTION)
    parser.add_argument('-i', '--input', help=INPUT_HELP)
    parser.add_argument('-o', '--output', help=OUTPUT_HELP)
    parser.add_argument('-s', '--server', default=BASE_URL, help=SERVER_HELP)
    parser.add_argument('-k', '--apikey', required='true', help=API_HELP)
    parser.add_argument('-m', '--marker', action='store_true', help=MARKER_HELP)
    parser.add_argument('-l', '--lang', default="ar-en", help=LANG_HELP)
    parser.add_argument('-d', '--domain', default="general-fast", help=DOMAIN_HELP)
    parser.add_argument('-v', '--verbose', action='store_true', help=VERBOSE_HELP)
    parser.add_argument('-n', '--skip', default=0, type=int, help=SKIP_HELP)

    return parser.parse_args()


def translate(text, base_url, apikey, langpair, domain):
    apikey = "key=" + apikey
    langpair = "langpair=" + langpair
    domain = "domain=" + domain
    text = "text=" + urllib.parse.quote(text.encode('utf-8'), safe='~()*!.\'')

    url = base_url + "translate?" + apikey \
          + "&" + langpair \
          + "&" + domain \
          + "&" + text

    res = requests.get(url)

    assert (res.status_code == 200)
    return res.json()["translatedText"]


def translate2(text, base_url, apikey, langpair, domain):
    apikey = "key=" + apikey
    langpair = "langpair=" + langpair
    domain = "domain=" + domain
    # text = "text=" + urllib.quote(unicode(text).encode('utf-8'), safe='~()*!.\'')
    text = "text=" + urllib.quote(text, safe='~()*!.\'')

    url = base_url + "translate?" + apikey \
          + "&" + langpair \
          + "&" + domain \
          + "&" + text

    res = requests.get(url)

    assert (res.status_code == 200)
    return res.json()["translatedText"]


'''
def main2():
    args = parse_args()

    if args.input:
        infile = codecs.open(args.input, encoding='utf-8')
    else:
        infile = codecs.getreader('utf-8')(sys.stdin)

    if args.output:
        outfile = codecs.open(args.output, 'a', encoding='utf-8')
    else:
        outfile = codecs.getwriter('utf-8')(sys.stdout)

    if args.lang != "ar-en" and args.lang != LANG_PAIRS:
        print "Illegal language pair"
        sys.exit(1)

    line_idx = 1
    with infile as fp:
        for line in fp:
            if line_idx <= args.skip:
                line_idx += 1
                continue

            if args.verbose:
                if line_idx % 10 == 0:
                    print 'Translating line %d [%s]'%(line_idx, line[:20])

            if args.marker:
                source = line[line.find(' ')+1:].strip()
            else:
                source = line.strip()

            target = translate(source, args.server, args.apikey, args.lang, args.domain)

            if args.marker:
                outfile.write(line[:line.find(' ')+1] + target + '\n')
            else:
                outfile.write(target + '\n')
            line_idx += 1

        outfile.close()
'''

def parseSrtTime(line):
    # 00:12:49,733 --> 00:12:52,389
    line = line.replace(",", ".").strip()
    times = line.split(" --> ")

    time = re.split(':|\.', times[0])
    startTime = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    startTime = "%d.%s" % (startTime, time[3])
    startTime = float(startTime)

    time = re.split(':|\.', times[1])
    endTime = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    endTime = "%d.%s" % (endTime, time[3])
    endTime = float(endTime)
    endTime -= 0.001

    return startTime, endTime


def getCtmSent(startTime, endTime, ctmLines, nofCtmLines):
    ctmSent = ""
    n = 0
    start = -1
    end = -1
    silenceAfterSent = 0.0
    for k in range(0, nofCtmLines - 1):
        if ctmLines[k].startswith("XXX"):
            continue
        ctmLine1 = ctmLines[k]
        fields1 = ctmLine1.split(" ")
        start1 = float(fields1[2])
        duration1 = float(fields1[3])
        word1 = fields1[4]
        confidence1 = float(fields1[5])

        ctmLine2 = ctmLines[k + 1]
        fields2 = ctmLine2.split(" ")
        start2 = float(fields2[2])
        duration2 = float(fields2[3])
        word2 = fields2[4]
        confidence2 = float(fields2[5])

        n += 1
        if (startTime >= start1 and startTime <= start2) or (n == 1 and startTime <= start1):
            for m in range(k, nofCtmLines):
                ctmLine3 = ctmLines[m]
                fields3 = ctmLine3.split(" ")
                start3 = float(fields3[2])
                duration3 = float(fields3[3])
                word3 = fields3[4]
                confidence3 = float(fields3[5])

                end3 = start3 + duration3
                if endTime <= end3:
                    silenceAfterSent = start3 - end
                    break

                silence = ""
                if m < nofCtmLines - 1:
                    ctmLine4 = ctmLines[m + 1]
                    fields4 = ctmLine4.split(" ")
                    start4 = float(fields4[2])
                    duration4 = float(fields4[3])
                    word4 = fields4[4]
                    confidence4 = float(fields4[5])

                    diff4 = start4 - end3
                    #if diff4 >= SILENCE_BETWEEN_WORDS:
                    #    #silence = "(%0.2f)" % diff4
                    #    silence = "$"
                ctmSent += word3 + silence + " "

                ctmLines[m] = "XXX" + ctmLines[m]
                if start == -1:
                    start = start3
                end = start3 + duration3
            break
    ctmSent = ctmSent.strip()

    #if len(ctmSent) > 0:
    #    if ctmSent.endswith("$"):
    #        ctmSent += "CORRECTEOS"
    #    else:
    #        ctmSent += "MISSEDEOS"

    return ctmSent, start, end, silenceAfterSent


def cleanSrt(sent):
    sent2 = sent
    sent2 = sent2.replace("  ", " ")

    # Remove empty tags
    sent2 = sent2.replace("[APPLAUSE]", "")
    sent2 = sent2.replace("[BREATH]", "")
    sent2 = sent2.replace("[HES]", "")
    sent2 = sent2.replace("[LAUGH]", "")
    sent2 = sent2.replace("[MUSIC]", "")
    sent2 = sent2.replace("[NOISE]", "")
    sent2 = sent2.replace("[UNK]", "")

    sent2 = sent2.replace("[FALSE ", "")
    sent2 = sent2.replace("[REP ", "")
    sent2 = sent2.replace("[INTERJ ", "")
    sent2 = sent2.replace("[GUESS:", "")
    sent2 = sent2.replace("[CORR ", "")
    sent2 = sent2.replace("[hes ", "")

    sent2 = sent2.replace("[NE:PER ", "")
    sent2 = sent2.replace("[NE:REP ", "")
    sent2 = sent2.replace("[NE:LOC ", "")
    sent2 = sent2.replace("[NE:ORG ", "")
    sent2 = sent2.replace("[NE:MISC ", "")
    sent2 = sent2.replace("[NE: PER ", "")
    sent2 = sent2.replace("[NE: LOC ", "")
    sent2 = sent2.replace("[NE: ORG ", "")

    # Remove empty tags
    sent2 = sent2.replace("[تصفيق]", "")
    sent2 = sent2.replace("[نفس]", "")
    sent2 = sent2.replace("[تردد]", "")
    sent2 = sent2.replace("[ضحك]", "")
    sent2 = sent2.replace("[موسيقى]", "")
    sent2 = sent2.replace("[ضجيج]", "")
    sent2 = sent2.replace("[مبهم]", "")

    sent2 = sent2.replace("[خطأ ", "")
    sent2 = sent2.replace("[تكرار ", "")
    sent2 = sent2.replace("[INTERJ ", "")
    sent2 = sent2.replace("[خمن:", "")
    sent2 = sent2.replace("[عدل:", "")
    sent2 = sent2.replace("[حرفي:", "")

    sent2 = sent2.replace("[علم:شخص ", "")
    sent2 = sent2.replace("[علم:شخص]", "")
    sent2 = sent2.replace("[علم:مكان ", "")
    sent2 = sent2.replace("[علم:منظمة ", "")
    sent2 = sent2.replace("[علم:آخر ", "")
    sent2 = sent2.replace("[علم:اخر ", "")
    sent2 = sent2.replace("[علم: شخص ", "")
    sent2 = sent2.replace("[علم: مكان ", "")
    sent2 = sent2.replace("[علم: منظمة ", "")

    sent2 = sent2.replace("]", "")

    error = ""
    if sent2.find("[") >= 0:
        error = "ERROR"
    elif sent2.find(":") >= 0:
        error = "WARNING"

    sent2 = sent2.strip()
    return sent2, error

def normalizeEnglishFile(inFilename):
    fin = io.open(inFilename, mode="r", encoding="utf-8")
    lines = fin.readlines()
    fin.close()
    nofLines = len(lines)

    for i in range(0, nofLines):
        line = lines[i].strip()
        line2 = line.lower()
        line2 = re.sub(r'[^a-zA-Z0-9_’% ]', '', line2)

        #trans2 = translate(line2, BASE_URL, MY_KEY, LANG_PAIRS, MT_SYSTEM)
        #print(line2 + "\t" + trans2)
        #print(trans2)

def normalizeArabicFile(inFilename):
    fin = io.open(inFilename, mode="r", encoding="utf-8")
    lines = fin.readlines()
    fin.close()
    nofLines = len(lines)

    for i in range(0, nofLines):
        line = lines[i].strip()

        line2 = normalizeString(line)
        print(line2)

def main():
    #normalizeEnglishFile("E:/Speech/WAWCorpus/en/test/analysis/srt.txt")
    #normalizeArabicFile("E:/Speech/WAWCorpus/en/test/analysis/ctmMicrosoft100MT.txt")

    inFilename = "E:/Speech/WAWCorpus/en/test/analysis/ctm-postEdit.txt"
    fin = io.open(inFilename, mode="r", encoding="utf-8")
    lines = fin.readlines()
    nofLines = len(lines)
    fin.close()
    for i in range(0, nofLines):
        line = lines[i].strip()
        trans = translate(line, BASE_URL, MY_KEY, LANG_PAIRS, MT_SYSTEM)
        print(trans)
    return

    '''
    target = translate("Hello, good morning!", BASE_URL, MY_KEY, LANG_PAIRS, MT_SYSTEM)
    print(target)

    target = translate(
        "سيُعرض في #كتارا ثلاث أفلام باكستانية بالتعاون مع سفارة جمهورية #باكستان الإسلامية لدى #قطر الدعوة عامة",
        BASE_URL, MY_KEY, "ar-en", MT_SYSTEM)
    print(target)

    target = translate(
        "سيُعرض في كتارا ثلاث أفلام باكستانية بالتعاون مع سفارة جمهورية باكستان الإسلامية لدى قطر الدعوة عامة",
        BASE_URL, MY_KEY, "ar-en", MT_SYSTEM)
    print(target)
    print ("---------------------------------------------")
    '''

    callMT = True
    refTrans = ctmTrans = ""
    if callMT:
        print("filename\tno.\terror\ttime (srt,ctm)\tsrt\tsrt (clean)\tctm\tsilence(ms)\tref MT\tref MT (clean)\tref MT (norm)\tsrt MT\tctm MT")

        inFoldernameMp4 = "%s/mp4" % inFoldername
        for inFilename in os.listdir(inFoldernameMp4):
            if (inFilename.startswith("x")):
                continue
            inFilename = inFilename.replace(".mp4", "")

            srtFilename = "%s/srt/%s.srt" % (inFoldername, inFilename)
            transFilename = "%s/trans/%s.trans" % (inFoldername, inFilename)
            ctmFilename = "%s/ctm/%s.ctm" % (inFoldername, inFilename)

            finCtm = io.open(ctmFilename, mode="r", encoding="utf-8")
            ctmLines = finCtm.readlines()
            finCtm.close()
            nofCtmLines = len(ctmLines)

            # parse translation
            allRefTranslations = {}
            finTrans = io.open(transFilename, mode="r", encoding="utf-8")
            lines = finTrans.readlines()
            finTrans.close()
            nofLines = len(lines)
            i = 0
            while i < nofLines:
                line = lines[i].strip()

                if line.find("-->") > 0:
                    startTime, endTime = parseSrtTime(line)
                    refTrans = ""
                    for j in range(i + 1, nofLines):
                        line2 = lines[j].strip()
                        if len(line2) == 0:
                            i = j
                            break
                        refTrans += " " + line2
                    refTrans = refTrans.strip()

                    allRefTranslations[line] = refTrans
                i += 1

            # parse ctm
            finSrt = io.open(srtFilename, mode="r", encoding="utf-8")
            lines = finSrt.readlines()
            finSrt.close()
            nofLines = len(lines)
            i = 0
            n = 0
            while i < nofLines:
                line = lines[i].strip()

                if line.find("-->") > 0:
                    startTime, endTime = parseSrtTime(line)
                    ctmSent, start, end, silenceAfterSent = getCtmSent(startTime, endTime, ctmLines, nofCtmLines)

                    refSent = ""
                    for j in range(i + 1, nofLines):
                        line2 = lines[j].strip()
                        if len(line2) == 0:
                            i = j
                            break
                        refSent += " " + line2
                    refSent = refSent.strip()
                    timeSpan = "%s (%f --> %f) , %f --> %f" % (line, startTime, endTime, start, end)

                    refSent2, errorRefSent2 = cleanSrt(refSent)
                    refTrans = translate(refSent2, BASE_URL, MY_KEY, LANG_PAIRS, MT_SYSTEM)
                    ctmTrans = translate(ctmSent, BASE_URL, MY_KEY, LANG_PAIRS, MT_SYSTEM)

                    refMT = allRefTranslations[line]
                    refMT2, errorRefMT2 = cleanSrt(refMT)
                    refMT3 = normalizeString(refMT2)

                    error = errorRefSent2 + errorRefMT2
                    n += 1
                    out = ""
                    if n == 1:
                        out = inFilename
                    out += "\t%d\t%s\t%s\t%s\t%s\t%s\t%0.2f\t%s\t%s\t%s\t%s\t%s" % (n, error, timeSpan, refSent, refSent2, ctmSent, silenceAfterSent, refMT, refMT2, refMT3, refTrans, ctmTrans)
                    print(out)

                i += 1


    sent = ""
    inFoldername = "E:/Speech/WAWCorpus/en/test"
    inFoldernameMp4 = "%s/mp4" % inFoldername
    for inFilename in os.listdir(inFoldernameMp4):
        #if (inFilename.endswith("_En.mp4") and inFilename.find("Theater-STE-002-PanelDiscussion_P3_En") >= 0):
        if (inFilename.endswith("_En.mp4") and not inFilename.startswith("x")):
            #print(inFilename)
            inFilename = inFilename.replace(".mp4", "")

            ctmFilename = "%s/ctm/%s.ctm" % (inFoldername, inFilename)
            if not os.path.exists(ctmFilename):
                print ("************* Error:" + ctmFilename)

            srtFilename = "%s/srt/%s.srt" % (inFoldername, inFilename)
            if not os.path.exists(srtFilename):
                print("************* Error:" + srtFilename)

            transFilename = "%s/trans/%s.trans" % (inFoldername, inFilename)
            if not os.path.exists(transFilename):
                print("************* Error:" + transFilename)

            #if True:
            #    continue

            finCtm = io.open(ctmFilename, mode="r", encoding="utf-8")
            lines = finCtm.readlines()
            start = duration = end = confidence = 0.0
            for line in lines:
                fields = line.split(" ")
                start = float(fields[2])
                duration = float(fields[3])
                word = fields[4]
                confidence = float(fields[5])

                if start - end >= SILENCE_BETWEEN_WORDS:
                    sent = sent.strip()
                    #if (len(sent) > 0):
                    #    print(sent)
                    sent = ""

                sent += word + " "

                end = start + duration
            #print("***********************")


if __name__ == '__main__':
    main()
