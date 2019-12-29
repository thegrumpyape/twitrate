import tweepy
import os
import requests

# Need to score each tweet with a rating, i.e 0 = Negative, 1 = Positive

def getTweets():
    url = 'http://localhost:5000/api/v1/tweets/ros'
    tweets = requests.get(url).json()
    return tweets['tweets']
    


if __name__ == '__main__':
    print('Model training will begin! First, we\'ll get the tweets...')
    tweets = getTweets()
