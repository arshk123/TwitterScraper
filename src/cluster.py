import pandas as pd
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
import mpld3
from nlp import tokenize_and_stem
from nlp import tokenize_only


def cluster(df, reduction=False):
        """
        df = sp_matrix
        reduction -> pca dimensional reduction
        """
        if reduction is True:
            df = df.toarray()
            pca = PCA(n_components=3).fit(df)
            X = pca.transform(df)
        else:
            X = df
        threshold = 3
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

def get_clusters(tweets, labels):
    clusters = {}
    for idx, val in enumerate(labels):
        if val in clusters:
            clusters[val].append(idx)
        else:
            clusters[val] = []
            clusters[val].append(idx)
        tweets[idx]['cluster'] = val


def print_cluster(tweets, clusters):
    for cluster in clusters.keys():
        for row in tweets:
            if row['cluster'] == cluster:
                print(row['tweet'])
        print("")
        print("")
        print("")


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


def main():
    # read csv into df
    df = pd.read_csv('../data/user_data/ArshKhandelwal_tweets.csv')
    tweets = df.to_dict('records')
    for tweet in tweets:
        tweet['tokenized_tweet'] = tokenize_only(tweet['tweet'])
        tweet['tokenize_stemmed_tweet'] = tokenize_and_stem(tweet['tweet'])
    sp_fv = vectorize(tweets)
    # 1 cluster tweets based on word frequency after dropping stop words
    labels, model, centroids = cluster(sp_fv, reduction=False)
    clusters = get_clusters(tweets, labels)
    print_cluster(tweets, clusters)
    # 2 NLP Sentiment analysis
    # 3 combine all hashtags from all tweets and determine overall sentiment of user

if __name__ == '__main__':
    main()
