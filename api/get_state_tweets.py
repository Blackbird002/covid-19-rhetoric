import twitterScraper as ts
import us_states_info as stateInfo
from pymongo import MongoClient
import datetime as dt
import sys
import os
import time

import sentiment_TextBlob as sT

'''
This script expects that mongoDB is installed and running...
'''

track_list = ["covid", "covid-19", "cdc", "pandemic"]

def create_tweet_entry(tweet):
    blob = sT.Text_Sentiment()
    polarity = blob.get_sentiment_polarity(tweet.text)
    tweetEntry = {
                    "key": tweet.tweet_id,
                    "sentiment": polarity
                }
    return tweetEntry

def run_scape():
    start_time = time.time()

    #Making a connection with MogoClient ()
    mongoDBclient = MongoClient("mongodb+srv://app:bigdata@cluster0-vejky.gcp.mongodb.net/test?retryWrites=true&w=majority")

    #Getting the DB (creates the DB if DNE)
    mongoDB = mongoDBclient['State_Tweets']

    #Gets state query info (cities and radii per state)
    stateDict = stateInfo.US_States_Info().get_US_cities_with_radius()

    for key in stateDict.keys():
        print("Scraping for:",key,"...")

        #Getting the collection (creates collection if DNE)
        mongoCollection = mongoDB[key]

        #For more tweets, change limit and poolsize
        tweets = ts.scrape_twitter(track_list=track_list, limit=80, poolsize=5, begindate=dt.date(2020, 1, 1), enddate=dt.date.today(),
                                   loc_near=stateDict.get(key).get('city'), radius=stateDict.get(key).get('radius'))

        ts.sort_tweets_by_popularity(tweets)

        mongoCollection.insert_many(map(create_tweet_entry,tweets))
        
        print("--- %s seconds ---" % (time.time() - start_time))