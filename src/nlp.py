import pandas as pd
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
from nltk.stem.snowball import SnowballStemmer


def cluster(tweets):
    for twt in tweets:
        print("dang I should really do this")

def tokenize_and_stem(text):
    stemmer = SnowballStemmer("english")
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out non alphabet
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def main():
    # read csv into df
    df = pd.read_csv('../data/hashtag_data/#DisruptTheNarrative_tweets.csv')
    tweets = df.to_dict('records')
    print(tweets[0].keys())

    # ['time', 'tweet', 'id', 'retweet_count', 'favorite_count', 'lang']
    for tweet in tweets:
        tweet['tokenized_tweet'] = tokenize_only(tweet['tweet'])
        tweet['tokenize_stemmed_tweet'] = tokenize_and_stem(tweet['tweet'])

    print(tweets[0]['tweet'])
    print(tweets[0]['tokenized_tweet'])


    # parse csv tweets one at a time
    # potential outputs
        # 1 cluster tweets based on word frequency after dropping stop words
        # 2 NLP Sentiment analysis
        # 3 combine all hashtags from all tweets and determine overall sentiment of user


if __name__ == '__main__':
    main()
