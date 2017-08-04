import string
import tweepy # https://github.com/tweepy/tweepy
import csv
import sys, getopt
import json


# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def read_json():
    with open('../api/api_keys.json') as js:
        data = json.load(js)
    api_keys = []
    api_keys.append(str(data['consumer_key']))
    api_keys.append(str(data['consumer_secret']))
    api_keys.append(str(data['access_key']))
    api_keys.append(str(data['access_secret']))
    return api_keys


def get_tweets(screen_name, api_keys):

    # Twitter auth codes
    auth = tweepy.OAuthHandler(api_keys[0], api_keys[1])
    auth.set_access_token(api_keys[2], api_keys[3])
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    # write the csv
    with open('../data/%s_tweets.csv' % screen_name, 'w+') as f:
        writer = csv.DictWriter(f, fieldnames = ["time", "tweet", "id", "retweet_count", "favorite_count", "lang"])
        writer.writeheader()
        for tweet in alltweets:
            json_str = tweet._json
            writer.writerow({'time': json_str["created_at"],
                            'tweet': json_str["text"],
                            'id': json_str["id"],
                            'retweet_count': json_str["retweet_count"],
                            'favorite_count': json_str["favorite_count"],
                            'lang': json_str["lang"]})


    f.close()
    pass

def main(argv):
    # print(argv)
    api_keys = read_json()
    get_tweets(argv, api_keys)

if __name__ == '__main__':
    # pass in the username of the account you want to download
    main(sys.argv[1])
