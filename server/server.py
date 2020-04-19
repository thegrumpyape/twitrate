import tweepy
import os
from dotenv import load_dotenv 
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("API_SECRET")
NUM_TWEETS = 50

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>TwitRate</h1>
<p>A prototype API for performing sentiment analysis on tweets</p>'''

@app.route('/api/v1/tweets/<string:query>', methods=['GET'])
def get_tweets(query):
    auth = tweepy.AppAuthHandler(API_KEY, SECRET_KEY)
    api = tweepy.API(auth)
    tweets = {}
    tweets["tweets"] = []

    for status in tweepy.Cursor(api.search, q=query, lang='en', tweet_mode='extended').items(NUM_TWEETS):
        if hasattr(status, 'retweeted_status'):
            try: 
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.full_text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.full_text
        tweets["tweets"].append(tweet)

    return tweets

app.run()