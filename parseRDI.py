import io
import re

dbgLineNo = 6927#6796 #215577
errors = 0
MAX_LEN = 1250
DELIM = [".", "،"]
#DELIM = ["."]

DIAC = ['َ', 'ُ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ّ', 'ْ']
def remove_diac(str):
    for ch in DIAC:
        if ch in str:
            str = str.replace(ch, "")

    return str

def clean_string(str):
    str2 = re.sub('\s+', ' ', str).strip()
    return str2


if False:
    errors = 0
    fin = io.open("D:/RDI/Kareem/all-text.txt.short", mode="rt", encoding="utf-8")
    for cnt, line in enumerate(fin):
        line2 = clean_string(line)
        line22 = remove_diac(line2)

        if len(line22) > MAX_LEN:
            errors += 1
            print("Line {}: Errors {}: {}".format(cnt, errors, line))
    fin.close()


filepath = "D:/RDI/Kareem/all-text.txt"
filepath1 = filepath + ".short"
filepath2 = filepath + ".short2"

fout1 = open(filepath1, "wt")
fout1 = io.open(filepath1, mode="wt", encoding="utf-8")
fout2 = io.open(filepath2, mode="wt", encoding="utf-8")

if False:
    fin = io.open(filepath, mode="rt", encoding="utf-8")
    for cnt, line in enumerate(fin):
        line2 = clean_string(line)
        line22 = remove_diac(line2)

        if len(line2) == 0:
            continue

        saved = False
        out = "%s\n" % line2
        if len(line22) > MAX_LEN:
            words2 = line2.split(" ")
            len2 = len(words2)

            index = -1
            for i in range(int(len2 / 2), len2):
                if words2[i].endswith("."):
                    index = i
                    break
            split = False
            if index > 0:
                s1 = s2 = ""
                for i in range(0, index + 1):
                    s1 += "%s " % words2[i]
                for i in range(index + 1, len2):
                    s2 += "%s " % words2[i]

                s12 = remove_diac(s1)
                s22 = remove_diac(s2)
                split = True

                len12 = len(s12)
                len22 = len(s22)

            if split and len12 <= MAX_LEN and len22 <= MAX_LEN:
                out = "XXX%s\nXXX%s\n" % (s1, s2)
                fout2.write(out)
                saved = True
            else:
                index = -1
                for i in range(int(len2 / 2), 0, -1):
                    if words2[i].endswith("."):
                        index = i
                        break
                split = False
                if index > 0:
                    s1 = s2 = ""
                    for i in range(0, index + 1):
                        s1 += "%s " % words2[i]
                    for i in range(index + 1, len2):
                        s2 += "%s " % words2[i]

                    s12 = remove_diac(s1)
                    s22 = remove_diac(s2)
                    split = True

                    len12 = len(s12)
                    len22 = len(s22)

                if split and len12 <= MAX_LEN and len22 <= MAX_LEN:
                    out = "YYY%s\nYYY%s\n" % (s1, s2)
                    fout2.write(out)
                    saved = True

            if not saved:
                fout1.write(out)
        else:
            fout2.write(out)
    fin.close()

    fout1.close()
    fout2.close()

fin = io.open(filepath, mode="rt", encoding="utf-8")
for cnt, line in enumerate(fin):

    # if cnt > 1000:
    #    break
    #if True or cnt % 1000 == 0:
    #    print("Line {}: Errors {}: {}".format(cnt, errors, line))

    if cnt == dbgLineNo:
        breakpoint = True

    line2 = clean_string(line)
    line22 = remove_diac(line2)

    # if len(line22) == 0:
    #    continue

    if len(line22) > MAX_LEN:
        line3 = line2.strip()
        out = "%s\n" % line3
        fout2.write(out)

        words2 = line2.split(" ")
        len2 = len(words2)
        line3 = ""
        i = 0
        lastStartIndex = 0
        skipLine = False
        while i < len2:
            w3 = words2[i]

            if len(line3) + len(w3) > MAX_LEN:
                EOS = False
                for delim in DELIM:
                    j = 0
                    for j in range(i, 1, -1):
                        w4 = words2[j]
                        if w4.endswith(delim):
                            line3 = ""
                            for k in range(lastStartIndex, j + 1):
                                w5 = words2[k]
                                line3 += "%s " % w5

                            if len(line3) == 0:
                                EOS = False
                                break

                            line3 = line3.strip()
                            line33 = remove_diac(line3)
                            if len(line33) > MAX_LEN:
                                pass
                                #errors += 1
                                #print("Errors: %d %s" % (errors, line3))
                            else:
                                out = "%s\n" % line3
                                fout1.write(out)

                                line3 = ""
                                lastStartIndex = j + 1
                                EOS = True
                                break
                        if EOS:
                            break
                if not EOS:
                    line3 = ""
                    skipLine = True
                    errors += 1
                    print("Line:%d Errors: %d %s" % (cnt, errors, line2))
                    break

                line3 = ""
                i = j
            else:
                line3 += "%s " % w3
            i += 1
            if skipLine:
                line3 = ""
                break

        if len(line3) > 0:
            line3 = line3.strip()
            out = "%s\n" % line3
            fout1.write(out)

            line33 = remove_diac(line3)
            if len(line33) > MAX_LEN:
                errors += 1
                print("Errors: %d %s" % (errors, line3))
    else:
        # out = "%s\n" % (line2)
        # fout1.write(out)
        pass

fin.close()
fout1.close()
fout2.close()