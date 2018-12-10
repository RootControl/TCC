from tweepy import Stream
from tweepy.streaming import StreamListener, json
from src.downloadTweets.DownloadTweets import auth
from src.database.DatabaseConnection import addTweet, creatingTable

# ###### Variables ###### #
databaseTable = "WorldCupRussia2018"
hashtag = "#WorldCupRussia2018"
# ####################### #


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            tweet = json.loads(data)  # transform the tweet in a dic
            creatingTable(databaseTable)
            addTweet(databaseTable, tweet['created_at'], tweet['id_str'], tweet['text'], tweet['user']['id_str'],
                     tweet['user']['name'], tweet['user']['screen_name'], tweet['user']['location'],
                     tweet['user']['description'], tweet['user']['lang'], tweet['lang'])
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=[hashtag])  # Capture all tweets by the hashtag
