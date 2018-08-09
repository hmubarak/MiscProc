import os, io, re, operator

NOF_WORDS = 3

filename = "D:/Arabic/CA/buckwalter.txt"
buckwalter = {}
fin = io.open(filename, mode="r", encoding="utf-8")
lines = fin.readlines()
# Decimal	Hex	Glyph	ASCII	Orthography
for line in lines:
    if not line.startswith('1'):
        continue
    parts = line.split("\t")
    buckwalter[parts[3]] = parts[2]
buckwalter[' '] = ' '

filename = "D:/Arabic/CA/suraList.txt"
suraList = {}
fin = io.open(filename, mode="r", encoding="utf-8")
lines = fin.readlines()
index = 1
for line in lines:
    suraList[index] = line.strip()
    suraList[index] = suraList[index].replace(" ", "-")
    index += 1

filename = "D:/Arabic/CA/quranic-corpus-morphology-0.4.txt"

errors = nofLines = 0
common = {}
common2 = {}

fin = io.open(filename, mode="r", encoding="utf-8")

filename2 = "D:/Arabic/CA/quranic-corpus-morphology-0.4-UTF8.txt"
#fout = io.open(filename2, mode="w", encoding="utf-8")

lines = fin.readlines()
lastSura = 1
lastVerse = 1
verseText = ""
for line in lines:
    if not line.startswith('('):
        continue
    nofLines += 1
    # LOCATION	FORM	TAG	FEATURES
    # (1:2:3:1)	rab~i	N	STEM|POS:N|LEM:rab~|ROOT:rbb|M|GEN
    parts = line.strip().split("\t")
    location = parts[0]
    form = parts[1]
    tag = parts[2]
    features = parts[3]

    location = location.replace("(", "")
    location = location.replace(")", "")
    parts2 = location.split(":")
    sura = parts2[0]
    verse = parts2[1]
    index = parts2[2]
    index2 = parts2[3]

    if verse != lastVerse:
        verseText = re.sub('\s+', ' ', verseText).strip()
        verseText2 = ""
        for ch in verseText:
            if ch in buckwalter:
                verseText2 += buckwalter[ch]
            else:
                breakpoint = True
        verseText2 = re.sub(r'[^ ء-ي]', '', verseText2)
        #fout.write ("%s-%d\t%s\n" %(suraList[int(lastSura)], int(lastVerse), verseText2))

        words = verseText.split(" ")
        nofWords = len(words)
        if nofWords >= NOF_WORDS:
            for i in range(0, nofWords - (NOF_WORDS - 1)):
                exp1 = ""
                exp1List = []
                for j in range(i, i + NOF_WORDS):
                    exp1 += " %s " % words[j]
                    exp1List.append(words[j])

                exp1 = re.sub('\s+', ' ', exp1).strip()
                if exp1 in common:
                    common[exp1] += "\t%s-%s:%d" % (sura, suraList[int(sura)], int(lastVerse))
                else:
                    common[exp1] = "%s-%s:%d" % (sura, suraList[int(sura)], int(lastVerse))

                exp1Sorted = ""
                for x in sorted(exp1List):
                    exp1Sorted += "%s " % x
                exp1Sorted = exp1Sorted.strip()
                exp12 = ""
                for ch in exp1:
                    if ch in buckwalter:
                        exp12 += buckwalter[ch]

                if exp1Sorted in common2:
                    common2[exp1Sorted] += "\t%s-%s:%d %s" % (sura, suraList[int(sura)], int(lastVerse), exp12)
                else:
                    common2[exp1Sorted] = "%s-%s:%d %s" % (sura, suraList[int(sura)], int(lastVerse), exp12)

        if False and nofWords >= 3:
            for i in range(0, nofWords - 2):
                exp2 = ""
                exp2List = []
                for j in range(i, i + 3):
                    exp2 += " %s " % words[j]
                    exp2List.append(words[j])

                exp2 = re.sub('\s+', ' ', exp2).strip()
                if exp2 in common:
                    common[exp2] += "\t%s-%s:%d" % (sura, suraList[int(sura)], int(lastVerse))
                else:
                    common[exp2] = "%s-%s:%d" % (sura, suraList[int(sura)], int(lastVerse))

                exp2Sorted = ""
                for x in sorted(exp2List):
                    exp2Sorted += "%s " % x
                exp2Sorted = exp2Sorted.strip()
                exp22 = ""
                for ch in exp2:
                    if ch in buckwalter:
                        exp22 += buckwalter[ch]

                if exp2Sorted in common2:
                    common2[exp2Sorted] += "\t%s-%s:%d %s" % (sura, suraList[int(sura)], int(lastVerse), exp22)
                else:
                    common2[exp2Sorted] = "%s-%s:%d %s" % (sura, suraList[int(sura)], int(lastVerse), exp22)

        verseText = form
        lastSura = sura
        lastVerse = verse
    else:
        if index2 == '1':
            verseText += " %s" % (form)
        else:
            verseText += "+%s" % (form)

    previousLocation = location

s = "اختلاف\tكلمات البحث\t"
for i in range(0, 10):
    s += "سورة%d\t" % (i + 1)
print(s)

types2 = sorted(common2.items(), key=operator.itemgetter(0), reverse=False)
for k, v in types2:
    if v.find("\t") > 0:
        verse = ""
        for ch in k:
            if ch in buckwalter:
                verse += buckwalter[ch]
            else:
                breakpoint = True
        verse2 = re.sub(r'[^ ء-ي]', '', verse)

        lists = []
        difference = ""
        hits = v.split("\t")
        for i in range(0, len(hits)):
            words = hits[i].split(" ")
            s = ""
            for j in range(1, len(words)):
                s += " %s " % (words[j])
            s = re.sub('\s+', ' ', s).strip()
            lists.append(s)

        for i in range(0, len(lists) - 1):
            for j in range(i + 1, len(lists)):
                if (lists[i] != lists[j]):
                    difference = "1"
                    break;

        #print ("%s\t%s\t%s\t%s" % (difference, verse, verse2, v))
        print ("%s\t%s\t%s" % (difference, verse2, v))

fin.close()
#fout.close()