import psycopg2
from tweepy.streaming import json

# ###### Variables ###### #
host = "localhost"
port = "5432"
databaseName = "db_tcc"
user = "luiz"
password = "luiz"


# ####################### #


def connect():
    query = "host=" + host + " port=" + port + " dbname=" + databaseName + " user=" + user + " password=" + password
    handle = psycopg2.connect(query)
    con = handle
    if not con:
        print("Database connection ERROR!")
        exit()
    else:
        return con


def addTweet(table, created_at, id_str, tweet_text, user_id_str, user_name, user_screen_name, user_location,
             user_description, user_lang, tweet_lang):
    con = connect()
    cursor = con.cursor()

    sql = f"insert into {table} (created_at, id_str, tweet_text, user_id_str, user_name, user_screen_name," \
          "user_location, user_description, user_lang, tweet_lang) " \
          "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (str(created_at), str(id_str), str(tweet_text), str(user_id_str), str(user_name),
                         str(user_screen_name), str(user_location), str(user_description), str(user_lang),
                         str(tweet_lang)))
    con.commit()  # update the database


def populatingTweetsTable(game):
    with open(f'TweetsPerGame/{game}.json', 'r') as f:  # open the file
        for line in f:
            tweet = json.loads(line)  # Transform in a dic
            # add in tweets table
            addTweet(game, tweet['created_at'], tweet['id_str'], tweet['text'], tweet['user']['id_str'],
                     tweet['user']['name'], tweet['user']['screen_name'], tweet['user']['location'],
                     tweet['user']['description'], tweet['user']['lang'], tweet['lang'])


def creatingTable(tableName):
    con = connect()
    cursor = con.cursor()

    sql = f"create table if not exists {tableName} (" \
          f"id serial primary key," \
          f"created_at text," \
          f"id_str text," \
          f"tweet_text text," \
          f"user_id_str text," \
          f"user_name text," \
          f"user_screen_name text," \
          f"user_location text," \
          f"user_description text," \
          f"user_lang text," \
          f"tweet_lang text);"
    cursor.execute(sql)
    con.commit()


def getAllTweets(tableName):
    con = connect()
    cursor = con.cursor()

    sql = f"select * from {tableName} order by id;"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

