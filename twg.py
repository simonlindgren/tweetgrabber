import tweepy
from tweepy import OAuthHandler
from datetime import datetime
import time
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError

print("\nTweetgrabber")
print("==============================================")

# My access keys and tokens
consumer_key = ""
consumer_secret = ""
access_secret = ""
access_token = "16366472-"

# Set up authorisation towards the API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Set up the project
projname = input("Project name? ") # Ask the user for this
outfile = (projname + "_output.json")
print ("Enter keywords as comma-separated strings, eg: monkey,#monkeytime,the monkey,#2018")
print("(Leave empty if you only want to stream based on user accounts)")
keywords = input("? ") # Ask the user for this
keywordlist = keywords.split(',') # Read the inputted string into a list
keywordlist = [i.strip() for i in keywordlist] # Strip any leading/trailing whitespace from list items
print ("Enter user accounts as comma-separated strings, eg: 759251,37706685,19701628")
print("(Leave empty if you only want to stream based on keywords)")
users = input("? ") # Ask the user for this
userlist = users.split(',') # Read the inputted string into a list
userlist = [i.strip() for i in userlist] # Strip any leading/trailing whitespace from list items

print(userlist)

# Prepare a counter
hacky_counter = []

# Note the starttime
starttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Started at " + str(starttime))

# Create a twitter listener
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        hacky_counter.append('.') # increase hacky counter
        if len(hacky_counter) <= 1:
            print("\rGrabbed " + str(len(hacky_counter)) + " tweet", end="")
            #time.sleep(1) # seems we need this to get the console output to print nicely
        else:
            print("\rGrabbed " + str(len(hacky_counter)) + " tweets", end="")
            #time.sleep(1) # seems we need this to get the console output to print nicely
        try:
            with open(outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: " % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

# Create a stream
twitter_stream = tweepy.Stream(auth, MyStreamListener())

# Start streaming and check for errors
while True:
    try:
        twitter_stream.filter(track=keywordlist, follow=userlist)
    except ProtocolError:
        #print(', then got a ProtocolError but persisted...')
        continue # too much coming in? oh well, reconnect and continue
    except (Timeout, ReadTimeoutError, ConnectionError) as exc:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\rResting 120 seconds, starting " + str(now), end="")
        time.sleep(120)
        print("\r                                                          [last pause was " + str(now)+"]")
