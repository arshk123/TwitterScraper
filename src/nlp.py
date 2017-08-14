import pandas as pd
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from sklearn.cluster import Birch
import mpld3
from nltk.stem.snowball import SnowballStemmer


def cluster(df, reduction=False):
        """
        df = sp_matrix
        reduction -> pca dimensional reduction
        """
        if reduction is True:
            df = df.toarray()
            pca = PCA().fit(df)
            X = pca.transform(df)
        else:
            X = df

        threshold = 1.5

        # eventually standardize parameter list as function argument and allow for different algorithms to be used
        model = Birch(threshold=threshold, n_clusters=None)
        out = model.fit_predict(X)

        labels = model.labels_
        subcluster_labels = model.subcluster_labels_
        centroids = model.subcluster_centers_

        # model = Birch
        # centroids = cluster centroids
        # out = set of labels
        return out, model, centroids

def print_cluster(tweets, labels):
    for idx, val in enumerate(tweets):
        print(labels[idx])
        print(val['tweet'])

def vectorize(tweets):
    """ function to generate features and then vectorize into sparse matrix """
    dv = feature_extraction.DictVectorizer()
    fv = []
    for tweet in tweets:
        features = {}
        for word in tweet['tokenized_tweet']:
            features[word] = 1
        fv.append(features)
    sp_fv = dv.fit_transform(fv)
    return sp_fv

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
    df = pd.read_csv('../data/user_data/ArshKhandelwal_tweets.csv')
    tweets = df.to_dict('records')

    # ['time', 'tweet', 'id', 'retweet_count', 'favorite_count', 'lang']
    for tweet in tweets:
        tweet['tokenized_tweet'] = tokenize_only(tweet['tweet'])
        tweet['tokenize_stemmed_tweet'] = tokenize_and_stem(tweet['tweet'])

    sp_fv = vectorize(tweets)
    labels, model, centroids = cluster(sp_fv)

    # TODO
    # parse csv tweets one at a time
    # potential outputs
        # 1 cluster tweets based on word frequency after dropping stop words DONE
        # 2 NLP Sentiment analysis
        # 3 combine all hashtags from all tweets and determine overall sentiment of user


if __name__ == '__main__':
    main()
