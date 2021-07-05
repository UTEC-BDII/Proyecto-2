import tweepy
import params
import tracker
import cleaner
import index
import time
from os import listdir, remove
from os.path import isfile, join

# You must be on code folder to run the program

def query(idx):
    exit = 1
    while exit != 0:
        print("Enter query text:")
        q = input()
        print("Enter max number of results:")
        k = int(input())
        results = index.retrieval(q, k, idx)
        index.showResults(results)
        print("Enter 0 to exit or any other number to input another query")
        exit = int(input())
        print()

if __name__ == '__main__':
    print("Choose action:")
    print("--------------")
    print("1. Load tweets and create index")
    print("2. Read index from text file")
    op = int(input())
    print()

    if (op == 1):
        remove(params.clean_path + params.tweetFilename) 
        remove(params.folder_path + params.tweetFilename) 
        file = open(params.clean_path + params.tweetFilename, "w") 
        file.close() 
        file = open(params.folder_path + params.tweetFilename, "w") 
        file.close() 

        print("Enter time limit (seconds) for tweet search:")
        time_limit = input()
        start_time = time.time()

        # Track tweets
        listener = tracker.TweetListener(params.folder_path + params.tweetFilename, start_time, int(time_limit))
        auth = tweepy.OAuthHandler(params.consumer_key, params.consumer_secret)
        auth.set_access_token(params.access_token, params.access_token_secret)
        stream = tweepy.Stream(auth, listener)
        
        listaTrack = []
        for k, v in params.tracklist.items(): 
            listaTrack = listaTrack + v

        stream.filter(track=listaTrack)

        # Clean raw teets
        path_in = params.folder_path 
        path_out = params.clean_path

        for f in listdir(path_in):
            file_in = join(path_in, f)    
            file_out = join(path_out, f)   
            if isfile(file_in):
                cleaner.parse_file(file_in, file_out)

        # Inverted index and queries
        idx = index.InvertedIndex("index.txt", "norms.txt")
        idx.createIndex()
        print()
        query(idx)

    elif (op == 2):
        print("Enter index filename:")
        filename = input()
        print("Enter norms filename:")
        normsfile = input()
        idx = index.InvertedIndex(filename, normsfile)

        if idx.load():
            query(idx)
        
    else:
        print("Option is not available")
