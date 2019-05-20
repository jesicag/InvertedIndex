import xml.etree.ElementTree as ET
from nltk import word_tokenize
import string
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
# =============================================================================
# QUERY PREPROCESSING
# QUERY(S) TOKENIZATION
# =============================================================================
def tokenizeQuery(queries):
    tokenQueri=[]
    translator=str.maketrans('','',string.punctuation)
    for i in range(len(queries)):
        queries[i] = queries[i].translate(translator)
        queries[i] = ''.join([i for i in queries[i] if not i.isdigit()])
        queries[i] = re.sub(r'^https?:\/\/.*[\r\n]*','', queries[i], re.MULTILINE)
        tokenQueri.append(word_tokenize(queries[i]))
    return tokenQueri
# =============================================================================
# QUERY(S) CASE FOLDING
# =============================================================================
def caseFoldingQuery(tokenQueri):
    for i in range(len(tokenQueri)):
        tokenQueri[i] = [query.lower() for query in tokenQueri[i]]
    return tokenQueri
# =============================================================================
# QUERY(S) STOPWORD
# =============================================================================
def stopwordRemovalQuery(tokenQueri):
    global newQueri
    newQueri=[]
    for i in range(len(tokenQueri)):
        filtered = [w for w in tokenQueri[i] if not w in stopwords.words('english')]
        newQueri.append(filtered)
    return newQueri
# =============================================================================
# QUERY(S) STEMMING
# =============================================================================
def stemmingQuery(newQueri):
    stemmer = PorterStemmer()
    global listQueri
    global uniqQueri
    listQueri=[]
    uniqQueri =[]
    for i in range (len(newQueri)):
        temp=[]
        for word in newQueri[i]:
            if(word != stemmer.stem(word)):
                word = stemmer.stem(word)
                temp.append(word)
            else:
                temp.append(word)
            #menghindari duplikasi kata
            if(word not in uniqQueri):
                uniqQueri.append(word)
        listQueri.append(temp)
        del temp
    return uniqQueri
# =============================================================================
# BIBLE PREPROCESSING
# READ FILE XML
# =============================================================================
def readBible(pathFile):
    tree = ET.parse(pathFile)
    return tree
# =============================================================================
# GET NAME OF BIBLE'S BOOK
# =============================================================================
def bibleBookName(pathFile):
    bibleBookName = []
    bible = readBible(pathFile)
    for node in bible.iter('div'):
        biblename = (node.attrib['bookName'])
        bibleBookName.append(biblename)
    return bibleBookName
# =============================================================================
# GET NUMBER OF BIBLE'S VERSES
# =============================================================================
def bibleNoVers(pathFile):
    global noVers
    noVers = []
    bible = readBible(pathFile)
    for node in bible.iter('verse'):
        versNo = (node.attrib['vname'])
        noVers.append(versNo)
    return noVers
# =============================================================================
# GET WORDS IN EVERY VERSE
# =============================================================================
def bibleVers(pathFile):
    bibleVersWord = []
    bible = readBible(pathFile)
    for word in bible.iter('verse'):
        bibleVersWord.append(word.text)
    return bibleVersWord
# =============================================================================
# TOKENIZATION
# =============================================================================
def tokenization(allTeks):
    translator = str.maketrans('','',string.punctuation)
    tokenize = []
    for i in range(len(allTeks)):
        allTeks[i] = allTeks[i].translate(translator)
        allTeks[i] = re.sub(r'^https?:\/\/.*', '', allTeks[i],re.MULTILINE)
        tokenize.append(word_tokenize(allTeks[i]))
    return tokenize
# =============================================================================
# CASE FOLDING
# =============================================================================
def caseFolding(tokenize):
    global caseFold
    caseFold=[]
    for i in range(len(tokenize)):
        for n in range(len(tokenize[i])):
            tokenize[i][n] = tokenize[i][n].lower()
        caseFold.append(tokenize[i])
    return caseFold
# =============================================================================
# STOPWORD
# =============================================================================
def checkStopword(sentence, stop_words):
    sentence = [w for w in sentence if not w in stop_words]
    return sentence
def stopwordRemove(textList):
    stop_words = set(stopwords.words('english'))
    text = []
    for i in range(len(textList)):
        text.append(checkStopword(textList[i], stop_words))
    return text
# =============================================================================
# STEMMING
# =============================================================================
def stemming(newText):
    stemmer = PorterStemmer()
    global listText
    listText=[]
    for i in range (len(newText)):
        for n in range(len(newText[i])):
            newText[i][n] = stemmer.stem(newText[i][n])
    return newText

def uniqueWords(listText):
    global uniqWords
    uniqWords = []
    for i in range (len(listText)):
        for n in range(len(listText[i])):
            if(listText[i][n] not in uniqWords):
                uniqWords.append(listText[i][n])
    return uniqWords
# =============================================================================
# INDEXING
# =============================================================================
def createIndex(newText, docno):
    terms = uniqueWords(newText)
    proximity = {}
    for term in terms:
        position = {}
        for n in range(len(newText)):
            if(term in newText[n]):
                position[docno[n]] = []
                for i in range(len(newText[n])):
                    if(term == newText[n][i]):
                        position[docno[n]].append(i)
        proximity[term] = position
    return proximity

# =============================================================================
# FIND QUERY IN INDEX TERMS
# =============================================================================
def queryInIndex(query, index):
    result = []
    for word in query:
        if word in index:
            result.append(word)
    return result
# =============================================================================
# DF
# =============================================================================
def df(query, index):
    docFreq = {}
    for word in query:
        if word in index.keys():
            docFreq[word] = len(index[word])
    return docFreq
# =============================================================================
# IDF
# =============================================================================
def idf(df, N):
    inv = {}
    for word in df:
        inv[word] = math.log10(N / df[word])
    return inv
# =============================================================================
# TF
# =============================================================================
def tf(query, index):
    termFreq = {}
    for word in query:
        freq = {}
        if word in index:
            for i in index[word]:
                freq[i] = len(index[word][i])
        termFreq[word] = freq
    return termFreq
# =============================================================================
# TF-IDF
# =============================================================================
def tfidf(tf, idf):
    w = {}
    for word in tf:
        wtd = {}
        for doc in tf[word]:
            wtd[doc] = (1 + (math.log10(tf[word][doc]))) * idf[word]
        w[word] = wtd
    return w
# =============================================================================
# SCORING
# =============================================================================
def score(TFIDF):
    res = {}
    for i in TFIDF:
        for j in TFIDF[i]:
            res[j] = 0
    for i in TFIDF:
        for j in TFIDF[i]:
            res[j] = res[j] + TFIDF[i][j]
    sorted_dict = sorted(res, key=res.get, reverse=True)[:10]
    return sorted_dict
# =============================================================================
# PROCESS FOR QUERY(S)
# =============================================================================
def processQuery(word):
    global g,h,j,queryStem
    queries = []
    for i in word:
        queries = word.split()
    g = tokenizeQuery(queries)
    h = caseFoldingQuery(g)
    j = stopwordRemovalQuery(h)
    queryStem = stemmingQuery(j)
    return queryStem

fileRSV = ('invertedIndex/mainFunction/bible_xml/RSV.xml')
bibleRSV = readBible(fileRSV)
bookNameRSV = bibleBookName(fileRSV)
noVersRSV = bibleNoVers(fileRSV)
versesRSV = bibleVers(fileRSV)
tokenRSV = tokenization(versesRSV)
caseFoldRSV = caseFolding(tokenRSV)
stopwordDelRSV = stopwordRemove(caseFoldRSV)
stemRSV = stemming(stopwordDelRSV)
uniqTermsRSV = uniqueWords(stemRSV)
indexRSV = createIndex(stopwordDelRSV, noVersRSV)
# =============================================================================
# PROCESS FOR DOCUMENTS
# =============================================================================
def mainRSV(textRSV):
    l = queryInIndex(processQuery(textRSV),indexRSV)
    print(l)
    N = len(noVersRSV)
    docFrequency = df(l, indexRSV)
    invDocFrequency = idf(docFrequency, N)
    termFrequency = tf(l, indexRSV)
    TFIDF = tfidf(termFrequency, invDocFrequency)
    sc = score(TFIDF)
    result = []
    for i in range(len(sc)):
        docLoc = noVersRSV.index(sc[i])
        result.append((noVersRSV[docLoc],versesRSV[docLoc]))
    return result