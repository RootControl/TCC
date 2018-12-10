# -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler
import json
from collections import Counter
from src.preprocessing.PreprocessingTokens import preprocess, stop


# ##### API variables to access the Twitter ###### #
consumer_key = 'xcohQpzc68K4tyI6iMORjiJX7'
consumer_secret = 'Q3DQ6TB1W3HVrOQOWPuAv1H60J4qqy5J67EXs4Mhx5URN75NsZ'
access_token = '967916796723507201-P1IL76UDiF1C2gRr0ZYJT4ROEPZQj2d'
access_secret = '3TRBR6RnB82Snf11MExheYF1tgR8hqMSXf3a7ZCpbD4bu'


consumer_key2 = '0KICI79nYvJLFGnq9Z98fQtBs'
consumer_secret2 = 'VIB9onzwvD44IH5DFF5w2JqziHnIyzQ0mR3qQ25xnbsyLzcCRv'
access_token2 = '1007093281824571393-4SMwEJsP2AfY7QWgvXcn1N6PuoUbUF'
access_secret2 = '17T2MW7MqiWMGJxR5369ZpWvwGLGKaHEFuJmEEQqUxNe9'
# ################################################ #

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

auth2 = OAuthHandler(consumer_key2, consumer_secret2)
auth2.set_access_token(access_token2, access_secret2)

api2 = tweepy.API(auth2)


def removeEmptyLines(game):
    with open(f'files/texts/{game}_ll.csv', encoding='utf-8') as inf, open(f'files/texts/{game}.csv', 'w', encoding='utf-8') as ouf:
        for line in inf:
            if not line.strip(): continue  # skip the empty line
            ouf.write(line)  # non-empty line. Write it to output


def getFrequentWords(game):
    with open(f'TweetDownloaded/streamListener{game}.json', 'r') as f:
        count_all = Counter()
        for line in f:
            tweet = json.loads(line)
            # Create a list with all the terms
            terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
            # Update the counter
            count_all.update(terms_stop)
        # Print the first 10 most frequent words
        print(count_all.most_common(10))


def printTokens(game):
    with open(f'TweetDownloaded/streamListener{game}.json', 'r') as f:
        for line in f:
            tweet = json.loads(line)  # Transform in a dic
            tokens = preprocess(tweet['text'])  # Take only the text
            print(tokens)


def printJSON(game):
    with open(f'files/{game}.json', 'r') as f:
        line = f.readline()  # read only the first tweet/line
        tweet = json.loads(line)  # load it as Python dict
        return json.dumps(tweet, indent=4)  # pretty-print
