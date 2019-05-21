"""
Created on Thu May  2 19:51:33 2019

"""
import xml.etree.ElementTree as ET
from nltk import word_tokenize
import string
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
from collections import OrderedDict
from operator import itemgetter
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
# EXPORT INDEX TO FILE
# =============================================================================
def exportIndex(index, filename):
    file = open(filename,'w')
    for n in index:
        file.write(n+'\n')
        for o in index[n]:
            file.write('\t'+o+': ')
            for p in range(len(index[n][o])):
                file.write(str(index[n][o][p]))
                if(p<len(index[n][o])-1):
                    file.write(', ')
                else:
                    file.write('\n')
    file.close()
    return "Index's file has been successfully created."
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
        inv[word] = math.log10(N/df[word])
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
            wtd[doc] = (1+(math.log10(tf[word][doc])))*idf[word]
        w[word] = (wtd)
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
            res[j] = res[j]+TFIDF[i][j]
    sorted_dict = OrderedDict(sorted(res.items(), key=itemgetter(1), reverse = True))#[:1])
    return sorted_dict
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
# CALL ALL FUNCTIONS
# =============================================================================
a = ('bible_xml/copy.xml')
b = readBible(a)
c = bibleBookName(a)
d = bibleNoVers(a)
e = bibleVers(a)
f = tokenization(e)
g = caseFolding(f)
h = stopwordRemove(g)
i = stemming(h)
j = uniqueWords(i)
k = createIndex(h,d)

line = "God said"
queries = []
for i in line:
    queries = line.split()
l = tokenizeQuery(queries)
m = caseFoldingQuery(l)
n = stopwordRemovalQuery(m)
o = stemmingQuery(n)

query = queryInIndex(o, j)
N = len(d)
docFrequency = df(o, k)
invDocFrequency = idf(docFrequency, N)
termFrequency = tf(o, k)
TFIDF = tfidf(termFrequency, invDocFrequency)   
sc = score(TFIDF)
sc
result = []
for i in range(len(sc)):    
    a = d.index(list(sc.keys())[i])
    x = list(sc.keys())[i]
    y = list(sc.values())[i]
    result.append((x,y,e[a]))
print(result)