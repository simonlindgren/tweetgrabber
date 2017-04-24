import tweepy
from datetime import datetime
print("\ntwEETgRABBER")

# My access keys and tokens
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Set up authorisation towards the API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up the api variable as our entry point for operations with the API
api = tweepy.API(auth)

# Set up the project
projname = input("Project name? ") # Ask the user for this
outfile = (projname + "_output.json") # Used on line 40 below
print ("Enter query as comma-separated strings, eg: monkey,#monkeytime,the monkey,#2018")
projquery = input("? ") # Ask the user for this
projquerylist = projquery.split(',') # Read the inputted string into a list
projquerylist = [i.strip() for i in projquerylist] # Strip any leading/trailing whitespace from list items
# projquerylist is used on line 53 below

starttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\nStreaming to " + outfile +" since " + str(starttime))
print("--> Check number of tweets in Terminal with: $ wc -l " + outfile)
print("--> ctrl + C to stop streaming")

# THE STREAMER ITSELF
from tweepy import Stream
from tweepy.streaming import StreamListener
 
class MyListener(StreamListener):
     
     def on_data(self, data):
        try:
            with open(outfile, 'a') as f:
                f.write(data)
                return True
                print("pip")
        except BaseException as e:
            print("Error on_data: " % str(e))
        return True
     
     def on_error(self, status):
        print(status)
        return True
        
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=projquerylist)