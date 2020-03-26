#!/usr/bin/env python3

'''
TWEETGRABBER
'''

import sqlite3
import tweepy
import json
from tweepy import OAuthHandler
from datetime import datetime
import time
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError
from credentials import consumer_key, consumer_secret, access_secret, access_token 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", default = "twg")
args = parser.parse_args()


logo='''
 ___                                         
  |       _   _ _|_  _  ._ _. |_  |_   _  ._ 
  | \/\/ (/_ (/_ |_ (_| | (_| |_) |_) (/_ |  
                     _|                         
  Written by Simon Lindgren <simon.lindgren@umu.se>                                                                         
'''

print(logo)

def main():
    dbcreate(args.project)
    stream(args.project)

def dbcreate(project):
    conn = sqlite3.connect(args.project + ".db")
    c = conn.cursor()
    c.execute("""CREATE TABLE tweets (
    id TEXT,
    created_at TEXT,
    author TEXT,
    author_location TEXT,
    author_followers INT,
    author_friends INT,
    hashtags TEXT,
    tweet TEXT,
    in_reply_to TEXT,
    lang TEXT,
    method TEXT,
    UNIQUE(id))
    """)
    conn.close()
    print("------- database created.\n")
    
    
# Set up the listener
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            conn = sqlite3.connect(args.project + ".db")
            data = json.loads(data)
            tweet_id = int(data['id'])
            tweet_created_at = data['created_at']
            tweet_author = data['user']['screen_name']
            author_location = data['user']['location']
            author_followers = data['user']['followers_count'] if not None else 0
            author_friends = data['user']['friends_count'] if not None else 0
            hashtags = data['entities']['hashtags']
            tweet_hashtags = []
            for hashtag in hashtags:
                tweet_hashtags.append("#" + str(hashtag['text']))
            tweet_hashtags = ",".join(tweet_hashtags)
            tweet_text = data['text']
            in_reply_to = data['in_reply_to_screen_name']
            tweet_lang = data['lang']
            conn.execute('INSERT INTO tweets (id, created_at, author, author_location, author_followers, author_friends, hashtags, tweet, in_reply_to, lang, method) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (tweet_id, tweet_created_at, tweet_author, author_location, author_followers, author_friends, tweet_hashtags, tweet_text, in_reply_to, tweet_lang, "StreamingAPI"))
            conn.commit()
            cursor = conn.cursor()
            cursor.execute("select * from tweets")
            r = cursor.fetchall()       
            print("\r======= Tweet from " + str(tweet_created_at[:-10]) + "(" + str(len(r)) +")", end="")
        except:
            pass
   
       
def stream(project):
    # Set query
    print ("------- enter keywords as comma-separated strings,")
    print ("------- eg: monkey,#monkeytime,#2020")
    print("------- (leave empty if only streaming based on user accounts)")
    keywords = input("------> ? ") # Ask the user for this
    keywordlist = keywords.split(',') # Read the inputted string into a list
    keywordlist = [i.strip() for i in keywordlist] # Strip any leading/trailing whitespace from list items
    print ("\n------- enter user accounts as comma-separated strings,")
    print ("------- eg: 759251,37706685,19701628")
    print("------- (leave empty if only streaming based on text query)")
    users = input("------> ? ") # Ask the user for this
    print("")
    userlist = users.split(',') # Read the inputted string into a list
    userlist = [i.strip() for i in userlist] # Strip any leading/trailing whitespace from list items
    
   # Authorise
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    # Setup stream
    twitter_stream = tweepy.Stream(auth, MyStreamListener())
    
    # Run stream
    twitter_stream.filter(track=keywordlist, follow=userlist)
    
    
if __name__ == '__main__':
    main()