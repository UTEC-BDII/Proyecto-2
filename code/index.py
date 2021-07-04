import numpy as np
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import json

from numpy.linalg.linalg import norm
import params

# Dictionary that contains tweets data for management on RAM
data = {}
with open(params.clean_path + params.tweetFilename, "r", encoding='utf-8') as read_file:
    data = json.load(read_file)

# Read list of stopwords
with open("stoplist.txt", 'r', encoding='utf-8') as file:
    stoplist = [line.lower().strip() for line in file]
stoplist += ['.', ',', '-', '«', '»', '(', ')', '"', '\'', ':', 
            ';', '!', '¡', '¿', '?', '`', '#', '@', '\'\'', '..',
            '...', '....', '``', '’']

# Remove stopwords
def clean(list):
    palabras_limpias = list[:]
    for token in list:
        if token in stoplist:
            palabras_limpias.remove(token)
    return palabras_limpias

# Reduce words
def stem(list):
    stemmer = SnowballStemmer('spanish')
    palabras_reducidas = []
    for token in list:
        palabras_reducidas.append(stemmer.stem(token))
    return palabras_reducidas

# Apply preprocessing on text
def getTerms(text):
    textTerms = word_tokenize(text.lower(), language="spanish")
    textTerms = clean(textTerms)
    textTerms = stem(textTerms)
    return textTerms

# Read data from all files on clean folder
def readData():
    tweets = {}
    cont = 0
    for elem in data:
        if elem["retweeted"] == True:
            text = elem["RT_text"]
        else:
            text = elem["text"]
        textTerms = getTerms(text)
        tweets[cont] = textTerms
        cont += 1

    return tweets

# TFIDF weight
# Get TFIDF vector from a terms list
def getTFIDF(termsList, idx, docID):
    vector = []
    termsUniq = list(dict.fromkeys(termsList))
    for term in termsUniq:
        if docID != -1:
            pub = idx[term]["pub"]
            for tuple in pub:
                if tuple[0] == docID:
                    wtf = tuple[1]
                    break
        else:
            tf = termsList.count(term)
            wtf = np.log10(tf)+1
        try:
            idf = idx[term]["idf"]
        except:
            idf = 0
        w = idf*wtf
        vector.append(w)
    
    if docID != - 1:
        return vector
    else:
        return termsUniq, vector

# Get norm of vector
def getNorm(vector):
    v = np.array(vector)
    return np.linalg.norm(v)

def retrieval(query, k):
    idx = InvertedIndex("index.txt")
    score = {}
    queryTerms = getTerms(query)
    queryTerms, queryW = getTFIDF(queryTerms, idx.index, -1)
    for i in range(len(queryTerms)):
        try:
            listPub = idx.index[queryTerms[i]]["pub"]
            idf = idx.index[queryTerms[i]]["idf"]
        except:
            listPub = []
            idf = 0
        for par in listPub:
            if not (par[0] in score):
                score[par[0]] = 0
            score[par[0]] += (idf * par[1]) * queryW[i]
    normas = idx.norms
    normQuery = getNorm(queryW)
    for docId in score:
        score[docId] = score[docId] / (normas[docId] * normQuery)
    
    result = [(i, j) for i, j in score.items()]
    result.sort(key = lambda tup : -tup[1])
    return result[:k]

# Show resulting tweets and its corresponding information
def showResults(results):
    print()
    if len(results) == 0:
        print("No results found for query")
        return

    print("Results in decreasing order of score:")
    print("-------------------------------------")
    for item in results:
        print("Score:", round(item[1], 3))
        tweet = data[item[0]]
        print("ID:", tweet['id'])
        print("User Name:", tweet['user_name'])
        print("Retweeted:", tweet['retweeted'])
        if (tweet['retweeted'] == True):
            print("RT User Name: ", tweet['RT_user_name'])
            print("RT Text: ", tweet['RT_text'])
        else:
            print("Text: ", tweet['text'])
        print("-------------------------------------")

# Inverted index class
class InvertedIndex:
    filename = ""
    index = {}
    norms = {}

    def __init__(self, filename):
        self.filename = filename
        self.createIndex()

    def createIndex(self):
        tweets = readData()
        N = len(tweets)
        tokens = []
        for tweet in tweets:
            for token in tweets[tweet]:
                tokens.append(token)
        
        tokensSet = set(tokens.copy())
        tokensSet = sorted(tokensSet)

        for token in tokensSet:
            tweetIDs = []
            for tweet in tweets:
                if token in tweets[tweet]:
                    tf = tweets[tweet].count(token)
                    tf = np.log10(tf)+1
                    tweetIDs.append([tweet, tf])
            idf = np.log10(N/len(tweetIDs))
            self.index[token] = {}
            self.index[token]["idf"] = idf
            self.index[token]["pub"] = tweetIDs

        self.getNorms(tweets)
        self.save()

    def getNorms(self, tweets):
        for tweet in tweets:
            termList = tweets[tweet]
            norm = getNorm(getTFIDF(termList, self.index, tweet))
            self.norms[tweet] = norm

    def save():
        return
