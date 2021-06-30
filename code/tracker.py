#Import the necessary methods from tweepy library
import tweepy
from datetime import datetime
import time

#This is a basic listener that just prints received tweets to stdout.
class TweetListener(tweepy.StreamListener):
    def __init__(self, base_filename, start_time, time_limit=60):
        self.__base_filename = base_filename
        self.time = start_time
        self.limit = time_limit

    def __open_file(self):
        now=datetime.now()
        filename = self.__base_filename
        ptrFile = open(filename, "a+")
        return ptrFile

    def on_data(self, data):
        if (time.time() - self.time) < self.limit:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " :: tweet read" )
            ptrFile = self.__open_file()        
            ptrFile.write(data + "\n")
            ptrFile.close()
            return True
        else: 
            print("Time limit passed.")
            return False

    def on_error(self, status):
        print("--- ERROR " + status + " ----")
        if status == 420:
            print("--- Waiting 15 minutes ---")
            time.sleep(15*60) #waiting by 15 minutes

