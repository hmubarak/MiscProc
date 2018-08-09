import os, io, re

folder = "D:\\Speech\\MGB2017\\YouTube\\EGY"

def normalize(txt):
    // From code: D:\PERL\CleanNames.pl
    $txt = ~ s / [ًٌٍَُِّـْ] // g;  ## removing diacritics and kashidas
    $txt = ~ tr / أآإىة / ااايه /;  ## normalizing standard characters
    ## normalizing Farsi characters
    $txt = ~ s / [ﻻﻵﻷעﻹﻼﻶﻸﬠ] / لا / g;
    $txt = ~tr /٠١٢۲٣۳٤٥Ƽ٦٧۷٨۸٩۹ﺀٴٱﺂﭑﺎﺈﺄιٲﺍٳίﺃٵﺇﺁﺑپﮨﺒٻﺐﺏﭘﭒﭗﭖﭚٮﭛٺﺗﭠﺘټﺖﺕﭡٹﭞٿﭟﭤﮢﭥﭨﭢﭣﮣﭧﺛﺜﮆﺚﺙٽﮇچﺟﭴﺠﭼڄڇﭸﺝڃﺞﭽﮀﭵﭹﭻﭾﭿﭺﺣﺤﺡﺢځﺧﺨڅڂﺦﺥڿډﺩڍﺪڊڈﮃﮂڋﮈڌﮉڐﮄﺫﺬڎڏۮڕړﺮﺭڒڔږڑژﮌڗﮍڙﺯﺰﮊﺳڛﺴﺲﺱښﺷڜﺸﺶﺵۺﺻﺼڝﺺﺹﺿﻀﺽڞﺾۻﻃﻁﻄﻂﻈﻇﻅڟﻆﻋ۶ﻌﻊﻉﻏﻐڠۼﻍﻎﻓڤﻔﭬڣﭰﻒﻑڦڢڡﭫڥﭪﭭﭯﭮﻗﻘڨﻖﻕڧﭱگڳکڪڱﮔﻛﮘڰﮐﮖﻜﮜڲﻚڴﮗڭﻙﮓﮙګڮﮕﮛڬﮎﮝﮚﮑﮒﮏﯖﯕﻟڵڷﻠڶﻞﻝڸﻣﻤﻢﻡﻧﻥڼﻨﻦڻڽﮠڹﮞںטּﮡﮟھہۃﮬﮪﮧۂﻫﮫﺔﻪﻬﮭﺓۿﻩەۀﮤﮥﮦۆۈۅﯙۉﻭﻮۄۋۇۊﯚٷٶﯛﯠﺆﯜۏﺅﯡﯝﯘﯢﯞﯣﯗﯟﯾےﻳۓېێﮱﻴﮯﭔﻲۑۍﯿﻱﻰﭜڀﺋﻯﭕﮮﺌﭓﯼﭝ༦ﺊﯽﮰﭙﯥﺉﯦﯧﯤیٸ / 012233455677
    8899
    ءءاااااااااااااااببببببببببببببتتتتتتتتتتتتتتتتتتتتثثثثثثثجججججججججججججججججججحححححخخخخخخخددددددددددددددذذذذذرررررررررررررزززسسسسسسششششششصصصصصضضضضضضططططظظظظظعععععغغغغغغفففففففففففففففففقققققققككككككككككككككككككككككككككككككككككللللللللممممننننننننننننننهههههههههههههههههههههوووووووووووووووووووووووووووويييييييييييييييييييييييييييييييييييييي /


errors = nofLines = nofWords = 0
uniqueWords = {}
for fname in os.listdir(folder):
    if (not fname.endswith(".txt") or fname.find("comments") < 0):
        continue
    filename = os.path.join(folder, fname)
    #print(filename)

    fin = io.open(filename, mode="r", encoding="utf-8")
    lines = fin.readlines()
    for line in lines:
        nofLines += 1
        line = line.replace("\\\"", "'")
        parts = line.split("\"")
        if len(parts) != 17:
            errors += 1
            continue
        orgText = parts[7]
        text = orgText.replace("\\n", " CTRLLF ")
        words = re.findall(r"[0-9a-zA-Zء-يً-ْ]+|[؟'.,!?;:،؛/\\<>()-+]", text)
        nofWords += len(words)
        print("%s\n%s" %(orgText, words))

        for w in words:
            if w in uniqueWords:
                uniqueWords[w] += 1
            else:
                uniqueWords[w] = 1

print("errors: %d, nofLines:%d, nofWords:%d, uniqueNofWords:%d" %(errors, nofLines, nofWords, len(uniqueWords)))
