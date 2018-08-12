import io
import re
import pandas as pd

LETTERS = ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك',
                    'ل', 'م', 'ن', 'ه', 'و', 'ي']
LETTERS_CONNECTED_NEXT = ['ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'ي']

DIAC_CODE_EMPTY = "0"
DIAC_CODE_FATHA = "1"
DIAC_CODE_KASRA = "2"
DIAC_CODE_DAMMA = "3"
DIAC_CODE_SUKUN = "4"
DIAC_CODE_FATHATAN = "5"
DIAC_CODE_KASRATAN = "6"
DIAC_CODE_DAMMATAN = "7"
DIAC_CODE_SHADDA = "9"
DIAC_CODE_SHADDA_FATHA = "A"
DIAC_CODE_SHADDA_KASRA = "B"
DIAC_CODE_SHADDA_DAMMA = "C"
DIAC_CODE_SHADDA_FATHATAN = "D"
DIAC_CODE_SHADDA_KASRATAN = "E"
DIAC_CODE_SHADDA_DAMMATAN = "F"

DIAC_CODES = {'َ':DIAC_CODE_FATHA, 'ِ':DIAC_CODE_KASRA, 'ُ':DIAC_CODE_DAMMA, 'ْ':DIAC_CODE_SUKUN, 'ً':DIAC_CODE_FATHATAN, 'ٍ':DIAC_CODE_KASRATAN, 'ٌ':DIAC_CODE_DAMMATAN, 'ّ':DIAC_CODE_SHADDA}
DIAC_CODES_SHADDA = {'َ':DIAC_CODE_SHADDA_FATHA, 'ِ':DIAC_CODE_SHADDA_KASRA, 'ُ':DIAC_CODE_SHADDA_DAMMA, 'ً':DIAC_CODE_SHADDA_FATHATAN, 'ٍ':DIAC_CODE_SHADDA_KASRATAN, 'ٌ':DIAC_CODE_SHADDA_DAMMATAN}
DIAC_CODES_TO_CHAR = {DIAC_CODE_EMPTY:'', DIAC_CODE_FATHA:'َ', DIAC_CODE_KASRA:'ِ', DIAC_CODE_DAMMA:'ُ', DIAC_CODE_SUKUN:'ْ', DIAC_CODE_FATHATAN:'ً', DIAC_CODE_KASRATAN:'ٍ', DIAC_CODE_DAMMATAN:'ٌ', DIAC_CODE_SHADDA:'ّ', DIAC_CODE_SHADDA_FATHA:'َّ', DIAC_CODE_SHADDA_KASRA:'َِ', DIAC_CODE_SHADDA_DAMMA:'ُّ', DIAC_CODE_SHADDA_FATHATAN:'ًّ', DIAC_CODE_SHADDA_KASRATAN:'ٍ', DIAC_CODE_SHADDA_DAMMATAN:'ٌّ'}

MAX_EXAMPLES = 4

def isArabicChar(ch):
    return re.search('[ء-ي]', ch)

# Commented method
#def isArabicDiac(ch):
#    return re.search('[ً-ْ]', ch)


def getDiacCodes(s):
    diacCodes = ""
    n = len(s)

    i = 0
    while i < n:
        ch = s[i]
        if not isArabicChar(ch):
            diacCodes = "ERROR"
            break

        diacCodes += ch

        step = 1
        code = DIAC_CODE_EMPTY

        ch2 = ''
        if i < n - 1:
            ch2 = s[i + 1]
        if ch2 in DIAC_CODES:
            code = DIAC_CODES[ch2]
            step = step + 1
            if code == DIAC_CODE_SHADDA:
                if i < n - 2:
                    ch3 = s[i + 2]
                    if ch3 in DIAC_CODES_SHADDA:
                        code = DIAC_CODES_SHADDA[ch3]
                        step = step + 1

        diacCodes += code;
        i = i + step

    return diacCodes;


def restoreWordFromDiacCodes(s, start, end):
    word = ""
    n = end
    for i in range(start, end):
        ch = s[i * 2]
        code = s[i * 2 + 1]

        word += ch
        word += DIAC_CODES_TO_CHAR[code]

    return word


def colorWord(lemmaDiacCodes, nofLemmaChar, start, end):
    s1 = s2 = s3 = ''
    s1 = restoreWordFromDiacCodes(lemmaDiacCodes, 0, start)
    s2 = restoreWordFromDiacCodes(lemmaDiacCodes, start, end)

    if end != nofLemmaChar:
        s3 = restoreWordFromDiacCodes(lemmaDiacCodes, end, nofLemmaChar)

    ch = lemmaDiacCodes[start * 2]
    prevCh = ''
    if (start != 0):
        prevCh = lemmaDiacCodes[(start - 1) * 2]

    kashida1 = "&zwj;"
    kashida2 = ""
    kashida3 = ""
    if prevCh in LETTERS_CONNECTED_NEXT:
        kashida2 = "&zwj;"
    if ch in LETTERS_CONNECTED_NEXT:
        kashida3 = "&zwj;"

    if len(s3) > 0:
        s = "<span style=\"color:black\">%s%s</span><span style=\"color:red\">%s%s%s</span><span style=\"color:black\">%s%s</span>" % (s1, kashida1, kashida2, s2, kashida1, kashida3, s3)
    else:
        s = "<span style=\"color:black\">%s%s</span><span style=\"color:red\">%s%s</span>" % (s1, kashida1, kashida2, s2)

    return s


def getCharShapes():
    letters_init = {}
    letters_middle = {}
    letters_final = {}

    GulfLemmaFreq_xls = pd.read_excel('D:/Arabic/Education/ArabicBooks/Gulf/GulfLemmaFreq.txt.merge-Eng.xlsx')

    #dfcols = ['order', 'percetage', 'lemma', 'lemma_undiac', 'source1', 'order1', 'freq1',
    #          'source2', 'order2', 'freq2', 'source3', 'order3', 'freq3', 'source4', 'order4', 'freq4', 'source5', 'order5', 'freq5', 'source6', 'order6', 'freq6']

    fout = open("D:\\Tmp\\AFL-charShapes.html", "wt", encoding="UTF8")

    nofLines = len(GulfLemmaFreq_xls)
    for i in range(0, nofLines):
        lemma = GulfLemmaFreq_xls['lemma'][i]
        lemma_undiac = GulfLemmaFreq_xls['lemma_undiac'][i]

        lemmaDiacCodes = getDiacCodes(lemma)
        nofLemmaChar = (int)(len(lemmaDiacCodes) / 2)
        if nofLemmaChar < 3:
            continue

        init = middle = last = ''
        for j in range(0, nofLemmaChar):
            ch = lemmaDiacCodes[j * 2]
            diac = lemmaDiacCodes[j * 2 + 1]

            if j == 0:
                init = ch
                words = ''
                if ch in letters_init:
                    words = letters_init[ch]
                count = words.count('،')
                if count < MAX_EXAMPLES - 1:
                    s = colorWord(lemmaDiacCodes, nofLemmaChar, j, j + 1)
                    if len(words) == 0:
                        letters_init[ch] = s
                    else:
                        letters_init[ch] = words + "، " + s
                    break
            elif j == nofLemmaChar - 1:
                last = ch
                words = ''
                if ch in letters_final:
                    words = letters_final[ch]
                count = words.count('،')
                if count < MAX_EXAMPLES - 1:
                    s = colorWord(lemmaDiacCodes, nofLemmaChar, j, j + 1)
                    if len(words) == 0:
                        letters_final[ch] = s
                    else:
                        letters_final[ch] = words + "، " + s
                    break
            else:
                middle = ch
                words = ''
                if ch in letters_middle:
                    words = letters_middle[ch]
                count = words.count('،')
                if count < MAX_EXAMPLES - 1:
                    s = colorWord(lemmaDiacCodes, nofLemmaChar, j, j + 1)
                    if len(words) == 0:
                        letters_middle[ch] = s
                    else:
                        letters_middle[ch] = words + "، " + s
                    break

    out = "</html>\n<p dir = \"rtl\">\n<table border=1 BORDERCOLOR=LIGHTGRAY>\n<tr>\n\t<th>Character</th><th>Initial</th><th>Middle</th><th>Final</th>\n</tr>\n"
    for ch in LETTERS:
        init = middle = final = ''
        if ch in letters_init:
            init = letters_init[ch]
        if ch in letters_middle:
            middle = letters_middle[ch]
        if ch in letters_final:
            final = letters_final[ch]

        out += "<tr>\n\t<th>%c</th><th>%s</th><th>%s</th><th>%s</th>\n</tr>\n" % (ch, init, middle, final)

    out += "</pr>\n</table>\n</html>"
    fout.write(out)
    fout.close()


def getCharDiac():
    letters_fatha = {}
    letters_damma = {}
    letters_kasra = {}

    GulfLemmaFreq_xls = pd.read_excel('D:/Arabic/Education/ArabicBooks/Gulf/GulfLemmaFreq.txt.merge-Eng.xlsx')

    #dfcols = ['order', 'percetage', 'lemma', 'lemma_undiac', 'source1', 'order1', 'freq1',
    #          'source2', 'order2', 'freq2', 'source3', 'order3', 'freq3', 'source4', 'order4', 'freq4', 'source5', 'order5', 'freq5', 'source6', 'order6', 'freq6']

    fout = open("D:\\Tmp\\AFL-charDiac.html", "wt", encoding="UTF8")

    nofLines = len(GulfLemmaFreq_xls)
    for i in range(0, nofLines):
        lemma = GulfLemmaFreq_xls['lemma'][i]
        lemma_undiac = GulfLemmaFreq_xls['lemma_undiac'][i]

        lemmaDiacCodes = getDiacCodes(lemma)
        nofLemmaChar = (int)(len(lemmaDiacCodes) / 2)
        if nofLemmaChar < 3:
            continue

        for j in range(0, nofLemmaChar):
            ch = lemmaDiacCodes[j * 2]

            diac = lemmaDiacCodes[j * 2 + 1]

            if diac == DIAC_CODE_FATHA:
                words = ''
                if ch in letters_fatha:
                    words = letters_fatha[ch]
                count = words.count('،')
                if count < MAX_EXAMPLES - 1:
                    s = colorWord(lemmaDiacCodes, nofLemmaChar, j, j + 1)
                    if len(words) == 0:
                        letters_fatha[ch] = s
                    else:
                        letters_fatha[ch] = words + "، " + s
                    break
            elif diac == DIAC_CODE_DAMMA:
                words = ''
                if ch in letters_damma:
                    words = letters_damma[ch]
                count = words.count('،')
                if count < MAX_EXAMPLES - 1:
                    s = colorWord(lemmaDiacCodes, nofLemmaChar, j, j + 1)
                    if len(words) == 0:
                        letters_damma[ch] = s
                    else:
                        letters_damma[ch] = words + "، " + s
                    break
            elif diac == DIAC_CODE_KASRA:
                words = ''
                if ch in letters_kasra:
                    words = letters_kasra[ch]
                count = words.count('،')
                if count < MAX_EXAMPLES - 1:
                    s = colorWord(lemmaDiacCodes, nofLemmaChar, j, j + 1)
                    if len(words) == 0:
                        letters_kasra[ch] = s
                    else:
                        letters_kasra[ch] = words + "، " + s
                    break

    out = "</html>\n<p dir = \"rtl\">\n<table border=1 BORDERCOLOR=LIGHTGRAY>\n<tr>\n\t<th>Character</th><th>Fatha</th><th>Damma</th><th>Kasra</th>\n</tr>\n"
    for ch in LETTERS:
        init = middle = final = ''
        if ch in letters_fatha:
            init = letters_fatha[ch]
        if ch in letters_damma:
            middle = letters_damma[ch]
        if ch in letters_kasra:
            final = letters_kasra[ch]

        out += "<tr>\n\t<th>%c</th><th>%s</th><th>%s</th><th>%s</th>\n</tr>\n" % (ch, init, middle, final)

    out += "</pr>\n</table>\n</html>"
    fout.write(out)
    fout.close()


if __name__ == '__main__':
    getCharShapes()
    getCharDiac()