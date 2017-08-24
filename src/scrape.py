import string
import tweepy # https://github.com/tweepy/tweepy
import csv
import sys, getopt
import json
import argparse
import db

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

class Scraper:
    def __init__(self):
        self.getCredentials()
        self.setupAuth()
        self.conn = db.getDBConnection()
    def getCredentials(self):
        with open('../config/config.json') as js:
            data = json.load(js)
            data = data['twitter_keys']
        api_keys = []
        api_keys.append(str(data['consumer_key']))
        api_keys.append(str(data['consumer_secret']))
        api_keys.append(str(data['access_key']))
        api_keys.append(str(data['access_secret']))
        self.api_keys = api_keys

    def setupAuth(self):
        auth = tweepy.OAuthHandler(self.api_keys[0], self.api_keys[1])
        auth.set_access_token(self.api_keys[2], self.api_keys[3])
        self.api = tweepy.API(auth)

    def get_hashtag_tweets(self, hash_tag, num_tweets):

        hash_tweets = tweepy.Cursor(self.api.search, q=hash_tag).items(num_tweets)
        cur = self.conn.cursor()
        with open('../data/hashtag_data/%s_tweets.csv' % hash_tag, 'w+') as f:
            writer = csv.DictWriter(f, fieldnames = ["time", "tweet", "id", "retweet_count", "favorite_count", "lang"])
            writer.writeheader()

            for tweet in hash_tweets:
                json_str = tweet._json
                writer.writerow({'time': json_str["created_at"],
                                'tweet': json_str["text"],
                                'id': json_str["id"],
                                'retweet_count': json_str["retweet_count"],
                                'favorite_count': json_str["favorite_count"],
                                'lang': json_str["lang"]})
                # write to db
                json_obj = {'time': json_str["created_at"],
                            'id': json_str["id"],
                            'retweet_count': json_str["retweet_count"],
                            'favorite_count': json_str["favorite_count"],
                            'lang': json_str["lang"]}
                json_str["text"] = json_str["text"].replace("'", "''")

                cur.execute('insert into hashtag_tweets (tweet, hash_tag, tweet_info) values (\'%s\', \'%s\', \'%s\')' % (json_str["text"], hash_tag, json.dumps(json_obj)))
                self.conn.commit()
        f.close()


    def get_user_tweets(self, screen_name):

        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

        cur = self.conn.cursor()
        # write the csv
        with open('../data/user_data/%s_tweets.csv' % screen_name, 'w+') as f:
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

                # write to db
                json_obj = {'time': json_str["created_at"],
                            'id': json_str["id"],
                            'retweet_count': json_str["retweet_count"],
                            'favorite_count': json_str["favorite_count"],
                            'lang': json_str["lang"]}
                json_str["text"] = json_str["text"].replace("'", "''")
                cur.execute('insert into user_tweets (tweet, user_name, tweet_info) values (\'%s\', \'%s\', \'%s\')' % (json_str["text"], screen_name, json.dumps(json_obj)))
                self.conn.commit()

        f.close()


def main(args):
    scrpr = Scraper()

    if args.username:
        scrpr.get_user_tweets(args.search_phrase)
    if args.hashtag:
        str = "#" + args.search_phrase
        scrpr.get_hashtag_tweets(hash_tag=str, num_tweets=10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="twitter scraping options")
    parser.add_argument('-u', '--username', action='store_true', help='Flag to indicate scraping of twitter account')
    parser.add_argument('-t', '--hashtag', action='store_true', help='Flag to indicate scraping of Hashtag (no hashtag required)')
    parser.add_argument('-s', '--search-phrase', help='Search term')
    args =  parser.parse_args()

    if not args.search_phrase:
        print("please specify a search phrase")
    else:
        # pass in the username of the account you want to download
        main(args)
