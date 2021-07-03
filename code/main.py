import tweepy
import params
import tracker
import cleaner
import index
import time
from os import listdir, remove
from os.path import isfile, join

# You must be on code/ folder to run the program

if __name__ == '__main__':
    """remove(params.clean_path + params.tweetFilename) 
    remove(params.folder_path + params.tweetFilename) 

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
            cleaner.parse_file(file_in, file_out)"""

    # Inverted index
    idx = index.InvertedIndex("index.txt")
    #print(idx.index)