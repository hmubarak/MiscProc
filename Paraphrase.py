import os, io, re, operator

filename = "D:\\Semantics\\ParaPhrase\\types.txt"

errors = nofLines = 0
types = {}

fin = io.open(filename, mode="r", encoding="utf-8")
lines = fin.readlines()
for line in lines:
    nofLines += 1
    # ب	ARAB	Y	111110100	111111111110111	PROG_PART	PROG_PART
    parts = line.strip().split("\t")
    for i in range(0, len(parts)):
        w = parts[i]
        if len(w) == 0:
            continue

        if w in types:
            types[w] += 1
        else:
            types[w] = 1

types2 = sorted(types.items(), key=operator.itemgetter(1), reverse=True)
for k, v in types2:
    print ("%s\t%d" % (k, v))
