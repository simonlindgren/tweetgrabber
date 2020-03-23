#!/usr/bin/env python3

'''
TWEETGRABBER TWITTER DATA EXTRACTOR
'''

from datetime import datetime
import pandas as pd
import shutil
import sqlite3
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", default = "twg")
args = parser.parse_args()

def main():
    now = datetime.now() # current date and time
    global nowstring
    nowstring = now.strftime("%Y_%m%d_%H%M")  + "_UTC"
    make_csv()
    
def make_csv():    
    # Read sqlite query results into a pandas DataFrame
    conn = sqlite3.connect(str(args.project) + ".db")
    tweets_df = pd.read_sql_query("SELECT * from tweets", conn)

    tweets_df = tweets_df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    tweets_df = tweets_df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    tweets_df = tweets_df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe

    tweets_df.to_csv(str(args.project) + "_" + nowstring + ".csv", index = False, encoding='utf-8')

if __name__ == '__main__':
    main()