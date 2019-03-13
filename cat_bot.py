import json
import os 
import praw
import requests
import time 
import tkinter 
import tweepy

consumer_key = ''
consumer_token = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_token)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()

for follower in tweepy.Cursor(api.followers).items():

    follower.follow()
    print ("Followed everyone that is following " + user.name)


def main_function():
    #subreddit = reddit_connection('cats')
    search_cats()
    

def reddit_connection(subred):
    print ("Setting up pathline to Reddit")
    red = praw.Reddit('yassob_python reddit twitter bot ' 'monitoring %s' %(subred))
    subreddit = red.get_subreddit(subred)
    return subreddit

def search_cats():

    keywords = ["cats", "kittens", "kitty","feline"]
    hatespeech = ["dislike", "hate", "despise", "terrible"]
    for searchterms in keywords: 
        search = searchterms
        #keep the tweets to a minimum so twitter doesnt ban me lol 
        numberOfTweets = 1
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                comment="@"+tweet.user.screen_name+" I like cats too :)"
                tweet.favorite()
                if not any(ext in str(tweet) for ext in hatespeech):
                    if not any(ext in tweet.user.screen_name for ext in keywords):
                        tweet.retweet()
                        api.update_status(comment, tweet.id)
                print('Retweeted and favorited the tweet')
                time.sleep(5)
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break

if __name__ == "__main__":
    main_function()
    
