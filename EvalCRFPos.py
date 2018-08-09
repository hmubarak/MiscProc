import os, io, re, operator

folder = "D:\\Dialect\\DialectPOSTagging\\CRFOutput2"
fullPOSTag = True

print("Word\trefPOS\tsysPOS\tcorrect\terror")

errors = nofLines = nofWords = correctWords = 0
errorTypes = {}
word = refPOS = sysPOS = ""
for fname in os.listdir(folder):
    #if (not fname.endswith(".txt") or fname.find("egy_") < 0):
    if (not fname.endswith(".txt")):
        continue
    filename = os.path.join(folder, fname)
    #print(filename)

    fin = io.open(filename, mode="r", encoding="utf-8")
    lines = fin.readlines()
    for line in lines:
        nofLines += 1
        # ب	ARAB	Y	111110100	111111111110111	PROG_PART	PROG_PART
        parts = line.split("\t")
        if len(parts) != 7:
            errors += 1
            continue
        w = parts[0]
        ref = parts[5]
        sys = parts[6].strip()

        if w == "WB":
            if len(word) == 0:
                continue
            nofWords += 1

            match = 0
            diff = ""
            if refPOS == sysPOS:
                match = 1
                correctWords += 1
            else:
                diff = "%s>%s" % (refPOS, sysPOS)
                refTokens = refPOS.split("+")
                sysTokens = sysPOS.split("+")
                if fullPOSTag and len(refTokens) > 1:
                    if diff in errorTypes:
                        errorTypes[diff] += 1
                    else:
                        errorTypes[diff] = 1
                else:
                    if not fullPOSTag and len(refTokens) == 1:
                        for i in range(0, len(refTokens)):
                            if refTokens[i] != sysTokens[i]:
                                diff = "%s>%s" % (refTokens[i], sysTokens[i])

                                if diff in errorTypes:
                                    errorTypes[diff] += 1
                                else:
                                    errorTypes[diff] = 1
                                break

            if True or match == 0:
                print("%s\t%s\t%s\t%d\t%s" % (word, refPOS, sysPOS, match, diff))
            word = refPOS = sysPOS = ""
            continue

        if len(refPOS) > 0:
            refPOS += "+"
            sysPOS += "+"
            word += "+"
        refPOS += ref
        sysPOS += sys
        word += w

print("errors: %d, nofLines:%d, nofWords:%d, correctWords:%d, accuracy = %s" %(errors, nofLines, nofWords, correctWords, "{:10.4f}".format(correctWords * 100 / nofWords)))

errorTypes2 = sorted(errorTypes.items(), key=operator.itemgetter(1), reverse=True)
totalErrors = 0
for k, v in errorTypes2:
    totalErrors += v

for k, v in errorTypes2:
    print ("%s\t%d\t%s" % (k, v, "{:10.1f}".format(float(v) * 100 / totalErrors)))
