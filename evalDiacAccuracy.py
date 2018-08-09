import io

urls = "D:/Arabic/Diac/WikiNews-DNN-Diac.txt"

fin = io.open(urls, mode="r", encoding="utf-8")
lines = fin.readlines()

diac_freq = {"a":0, "u":0, "i":0, "o":0, "#":0, "~a":0, "~u":0, "~i":0, "F":0, "N":0, "K":0, "~F":0, "~N":0, "~K":0}
diac_freq_correct = {"a":0, "u":0, "i":0, "o":0, "#":0, "~a":0, "~u":0, "~i":0, "F":0, "N":0, "K":0, "~F":0, "~N":0, "~K":0}
diac_freq_incorrect = {"a":0, "u":0, "i":0, "o":0, "#":0, "~a":0, "~u":0, "~i":0, "F":0, "N":0, "K":0, "~F":0, "~N":0, "~K":0}

i = correct = total = 0
for line in lines:
    i += 1
    if i == 1:
        continue

    line = line.strip()
    fields = line.split("\t")
    word = fields[0].strip()
    pred = fields[1].strip()
    truth = fields[2].strip()

    if pred == truth:
        correct += 1
    total += 1

    diac_freq[truth] += 1

    if truth == pred:
        diac_freq_correct[truth] += 1
    else:
        diac_freq_incorrect[truth] += 1

print("Correct:%d/%d, Accuracy = %0.3f, Error = %0.3f" % (correct, total, (correct * 100.0 / total), 100.0 - (correct * 100.0 / total)))

for diac in diac_freq:
    print("%s\t%d\t%d\t%d" % (diac, diac_freq[diac], diac_freq_correct[diac], diac_freq_incorrect[diac]))
#print(diac_freq)
