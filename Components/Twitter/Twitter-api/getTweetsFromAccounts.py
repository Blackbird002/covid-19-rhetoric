import pythonTwitterAPI as pt
import json
import os
from pymongo import MongoClient

'''
https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
'''

'''
Extended_tweet:

tweet = {
          'tweet_id':        item.id,
          'name':            item.user.name,
          'screen_name':     item.user.screen_name,
          'retweet_count':   item.retweet_count,
          'text':            item.full_text,
          'mined_at':        datetime.datetime.now(),
          'created_at':      item.created_at,
          'favourite_count': item.favorite_count,
          'hashtags':        item.entities['hashtags'],
          'status_count':    item.user.statuses_count,
          'location':        item.place,
          'source_device':   item.source
        }
'''

#########################################################
  # Function main
#########################################################

def main():
  os.system("sudo systemctl start mongod")

  print("****************************************************************")
  print("                           Warning:                             ")
  print("100,000 requests per day to the /statuses/user_timeline endpoint")
  print("Requests / 15-min window (app auth)	1500")
  print("****************************************************************")

  #Making a connection with MogoClient
  mongoDBclient = MongoClient('localhost', 27017)

  #Getting the DB (creates the DB if DNE)
  mongoDB = mongoDBclient['FunnyAccounts']

  #Getting the collection (creates collection if DNE)
  tweetsFromUsersCollection = mongoDB['FunnyAccountTweets']

  twitter_client = pt.TwitterClient()
  tweet_analyzer = pt.TweetAnalyzer()

  api = twitter_client.get_twitter_client_api()

  #List of Twitter Accounts to pull timeline from
  twitterTargetAccounts = ["someecards", "SpeakComedy", "TheComedyHumor", "FactsOfSchool", "wordstionary", "nbcsnl", "TheWorldOfFunny",
                           "holdmyale", "SignsFun"]

  #https://towardsdatascience.com/tweepy-for-beginners-24baf21f2c25
  for accout in twitterTargetAccounts:
      timeline = twitter_client.get_user_timeline_tweets(accout, 100)
      
      for tweet in timeline:

        #Send text section for sentiment tweet.full_text
        tweetEntry = {
          "tweetID": tweet.id,  
          "likes": tweet.favorite_count,
          "retweets": tweet.retweet_count,
          "sentiment_score" : 0
        }

        tweetsFromUsersCollection.insert_one(tweetEntry) 

  print("Done!")

if  __name__ == "__main__":
  main()