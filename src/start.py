import string
import csv
import sys, getopt
import json

#TODO make this starting point for both scraping and nlp
def main(args):
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
