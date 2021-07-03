import numpy as np
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import json
import params

# Consideration: since tweets, unlike documents, have a character limit () it would not 
# be a problem to read a whole tweet on RAM during preprocessing

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

# Read data from all files on clean folder
def readData():
    with open(params.clean_path + params.tweetFilename, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)

    tweets = {}
    cont = 0
    for elem in data:
        if elem["retweeted"] == True:
            text = elem["RT_text"]
        else:
            text = elem["text"]
        text = word_tokenize(text.lower(), language="spanish")
        text = clean(text)
        text = stem(text)
        tweets[cont] = text
        cont += 1

    return tweets

# Get TFIDF vector from a terms list
def getTFIDF(list, index):
    open = []
    return open

# Get norm of vector
def getNorm(vector):
    return 0

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
                    tf = round(np.log10(tf)+1, 3)
                    tweetIDs.append([tweet, tf])
            idf = round(np.log10(N/len(tweetIDs)), 3)
            self.index[token] = {}
            self.index[token]["idf"] = idf
            self.index[token]["pub"] = tweetIDs

        self.getNorms(tweets)

    def getNorms(self, tweets):
        for tweet in tweets:
            termList = tweets[tweet]
            norm = getNorm(getTFIDF(termList, self.index))
            self.norms[tweet] = norm