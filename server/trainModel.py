import nltk
import string
import numpy as np
import pandas as pd
import emoji
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
from bs4 import BeautifulSoup
from future.utils import iteritems
import re

# Turns words into their root word (dogs -> dog)
wordnet_lemmatizer = WordNetLemmatizer()

# Get common words that are removed from queries
stopwords = set(stopwords.words('english'))

# Initial reading and preprocessing
saData = pd.read_csv('./Sentiment Analysis Dataset.csv', error_bad_lines=False)
saData = saData.replace([np.inf, -np.inf], np.nan)
saData = saData.dropna()
saData = saData.sample(frac=1) # Shuffle data

# Get positive vs negative tweets
positiveTweets = saData[saData['Sentiment'] == 1]['SentimentText'].head(5000)
negativeTweets = saData[saData['Sentiment'] == 0]['SentimentText'].head(5000)

print(positiveTweets)
print(negativeTweets)

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
    # remove the # in each hashtagged word
    tweetList = re.sub(r'#([^\s]+)', r'\1', tweetList)
    # Separate the emojis from the string
    em_split_emoji = emoji.get_emoji_regexp().split(tweetList)
    em_split_emoji = [e for e in em_split_emoji if e in emoji.UNICODE_EMOJI]
    # Remove all emojies from tweet string
    tweetList = tweetList.encode('ascii', 'ignore').decode('ascii')
    # remove repeated characters
    tweetList = word_tokenize(tweetList)
    # Add emojies to end of list
    tweetList = tweetList + em_split_emoji
    return tweetList

# Create word index map dictionary
word_index_map = {}
current_index = 0

# Save tokens for second loop
positive_tokenized = []
negative_tokenized = []

# Add tokens from positive tweets to word index map
for tweet in positiveTweets:
    tokens = preprocess_tweet(tweet)
    positive_tokenized.append(tokens)
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1

# Add tokens from negative tweets to word index map
for tweet in negativeTweets:
    tokens = preprocess_tweet(tweet)
    negative_tokenized.append(tokens)
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1

def tokens_to_vector(tokens, label):
    # Create feature vector by adding the frequency of each word in map to the vector
    x = np.zeros(len(word_index_map) + 1) # last element is for the label
    for t in tokens:
        i = word_index_map[t]
        x[i] += 1
    # Normalize x
    x = x / x.sum()
    # Assign the label to the last element of the feature vector
    x[-1] = label
    return x

N = len(positive_tokenized) + len(negative_tokenized)
data = np.zeros((N, len(word_index_map) + 1))
i = 0
for tokens in positive_tokenized:
    xy = tokens_to_vector(tokens, 1)
    data[i,:] = xy
    i += 1

for tokens in negative_tokenized:
    xy = tokens_to_vector(tokens, 0)
    data[i,:] = xy
    i += 1

np.random.shuffle(data)

X = data[:,:-1]
Y = data[:,-1]

Xtrain = X[:-7000,]
Ytrain = Y[:-7000,]
Xtest = X[-3000:,]
Ytest = Y[-3000:,]

model = LogisticRegression()
model.fit(Xtrain, Ytrain)
print("Train accuracy:", model.score(Xtrain, Ytrain))
print("Test accuracy:", model.score(Xtest, Ytest))

# weights for each word
threshold = 0.5
for word, index in iteritems(word_index_map):
    weight = model.coef_[0][index]
    if weight > threshold or weight < -threshold:
        print(word, weight)
