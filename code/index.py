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
            '...', '....', '``']

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

# Inverted index class
class InvertedIndex:
    filename = ""
    index = {}

    def __init__(self, filename):
        self.filename = filename
        self.createIndex()

    def createIndex(self):
        tweets = readData()
        tokenFreq = []
        tokens = []
        for tweet in tweets:
            for token in tweets[tweet]:
                tokens.append(token)
        
        tokensSet = set(tokens.copy())
        for token in tokensSet:
            tokenFreq.append([token, tokens.count(token)])

        tokenFreq = sorted(tokenFreq)

        for token in tokenFreq:
            docIDs = []
            for tweet in tweets:
                if token[0] in tweets[tweet]:
                    docIDs.append(tweet)
            self.index[token[0]] = [token[1], docIDs]
            
        # self.write()