import tweepy
import emoji
import os
import functools
import operator
import requests
import re
import string
import numpy as np
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.decomposition import TruncatedSVD


'''
  Part 1: Get and preprocess all of the tweets that we need given the hashtag.
          Emojies are extracted and added to the end of the string for now.
'''

# test = 'Quarantine Time 😷🦠🧪⚠️ Due to #COVID19 I will be sending $750 - $9,000 to the first 500 people to like &amp; retweet this 🖤 ( comment  your cashapp,dm WhatsApp (402)\xa0989-0764 cashappinbio #Cashappfriday #Cashappblessing https://t.co/vXz81xnNPb'

hashtag = 'mondaythoughts'
stopwords = set(stopwords.words('english'))

def preprocess_tweet(text):
    # Check characters to see if they are in punctuation
    tweetList = [char for char in text if char not in string.punctuation]
    # Join the characters again to form the string.
    tweetList = ''.join(tweetList)
    # convert text to lower-case
    tweetList = tweetList.lower()
    # remove URLs
    tweetList = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', tweetList)
    tweetList = re.sub(r'http\S+', '', tweetList)
    # remove usernames
    tweetList = re.sub('@[^\s]+', '', tweetList)
    # Remove the word in the tweet that contains the original hashtag
    tweetList = re.sub(r'' + hashtag, "", tweetList)
    # remove the # in each hashtagged word
    tweetList = re.sub(r'#([^\s]+)', r'\1', tweetList)
    # Separate the emojis from the string
    em_split_emoji = emoji.get_emoji_regexp().split(tweetList)
    em_split_emoji = [e for e in em_split_emoji if e in emoji.UNICODE_EMOJI]
    # Remove all emojies from tweet string
    tweetList = tweetList.encode('ascii', 'ignore').decode('ascii')
    # remove repeated characters
    tweetList = word_tokenize(tweetList)
    # remove short words, they're probably not useful
    tweetList = [t for t in tweetList if len(t) > 2]
    # Add emojies to end of list
    tweetList = tweetList + em_split_emoji
    # remove stopwords from final word list
    return [word for word in tweetList if word not in stopwords]

# Gather the tweets
url = 'http://localhost:5000/api/v1/tweets/' + hashtag
tweets = requests.get(url).json()
tweets = tweets['tweets']

newTweets = []
index_word_list = []
word_index_map = {}
current_index = 0
# Preprocess tweets and save tokenized version
for tweet in tweets:
    processedTweet = preprocess_tweet(tweet) 
    newTweets.append(processedTweet)
    # Create word-to-index map from tokenized tweet
    for token in processedTweet:
      if token not in word_index_map:
          word_index_map[token] = current_index
          current_index += 1
          index_word_list.append(token)

# Creates a map of original tweets and preprocessed tweet lists. Used for debugging
tweet_mapping = {}
for k, v in zip(tweets, newTweets):
  tweet_mapping[k] = v
print(tweet_mapping)

'''
  Part 2: Cluster our tweet data and assign each tweet to one of two clusters
  
  *** Use Latent Semantic Analysis for this part ***
'''

# now let's create our input matrices - just indicator variables for this example - works better than proportions
def tokens_to_vector(tokens):
    x = np.zeros(len(word_index_map))
    for t in tokens:
        i = word_index_map[t]
        x[i] = 1
    return x

N = len(newTweets)
D = len(word_index_map)
X = np.zeros((D, N)) # terms will go along rows, documents along columns
i = 0
for tokens in newTweets:
    X[:,i] = tokens_to_vector(tokens)
    i += 1

svd = TruncatedSVD()
Z = svd.fit_transform(X)
plt.scatter(Z[:,0], Z[:,1])
for i in range(D):
    plt.annotate(s=index_word_list[i], xy=(Z[i,0], Z[i,1]))
plt.show()