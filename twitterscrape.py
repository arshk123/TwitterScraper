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

def determine_positivity(screen_name):
    print("Determining positivity")
    with open('%s_tweets.csv' % screen_name, 'r') as f:
        reader = csv.DictReader(f)
        # reader2 = csv.reader(f, delimiter=',')
#        for row in reader:
            # print(row['time'])

    f.close()
    pass

def get_tweets(screen_name):
    # Currently, this will only read my tweets (JK, I'll find someone worthwhile)

    #Twitter auth (creds to Rony)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
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
    with open('%s_tweets.csv' % screen_name, 'w+') as f:
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

    # “created_at”
    # “id”
    # “text”
    # “user_mentions”
    # “time_zone”
    # “retweet_count”
    # “favorite_count”
    # “lang"
    f.close()
    determine_positivity(screen_name)

    pass

def main(argv):
    # print(argv)
    get_tweets(argv)

if __name__ == '__main__':
    # pass in the username of the account you want to download
    main(sys.argv[1])
