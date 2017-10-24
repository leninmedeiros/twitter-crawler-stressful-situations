
import configparser
import tweepy
from pymongo import MongoClient
import sys
import json
import csv
import datetime
import random

CONFIG_FILE = '.config'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

consumer_key = config.get('TwitterConsumerKey', 'twitter_consumer_key')
consumer_secret = config.get(
    'TwitterConsumerSecret', 'twitter_consumer_secret'
    )
access_token = config.get('TwitterAccessToken', 'twitter_access_token')
access_token_secret = config.get(
    'TwitterAccessTokenSecret', 'twitter_access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

db_name = config.get('DB_Name', 'db')
server = config.get('DB_Server', 'server')
port = config.get('DB_Port', 'port')
username = config.get('DB_Username', 'username')
password = config.get('DB_Password', 'password')

db = MongoClient(host=server, port=int(port))
db[db_name].authenticate(username, password)

RELATIONSHIPS_QUERIES = [
    'relationship :(', 'girlfriend :(', 'boyfriend :(', 'wife :(',
    'husband :(', 'crush :(', 'relationship #stressed',
    'girlfriend #stressed', 'boyfriend #stressed', 'wife #stressed',
    'husband #stressed', 'crush #stressed'
]

WORK_QUERIES = [
    'work :(', 'job :(', 'project :(', 'workload :(', 'office :(', 'boss :(',
    'work #stressed', 'job #stressed', 'project #stressed',
    'workload #stressed', 'office #stressed', 'boss #stressed'
]

DEATH_QUERIES = [
    'died :(', '"passed away" :(', 'rip :(', '"rest in peace" :(',
    'funeral :(', 'death :(', 'died #stressed', '"passed away" #stressed',
    'rip #stressed', '"rest in peace" #stressed', 'funeral #stressed',
    'death #stressed'
]

FINANCES_QUERIES = [
    'money :(', 'debts :(', 'salary :(', 'expenses :(', 'dollars :(',
    'euros :(', 'money #stressed', 'debts #stressed', 'salary #stressed',
    'expenses #stressed', 'dollars #stressed', 'euros #stressed'
]

HEALTH_QUERIES = [
    'disease :(', 'ill :(', 'hospital :(', 'sick :(', 'diagnosed :(',
    'health :(', 'disease #stressed', 'ill #stressed', 'hospital #stressed',
    'sick #stressed', 'diagnosed #stressed', 'health #stressed'
]

SCHOOL_QUERIES = [
    'exams :(', 'test :(', 'grade :(', 'teacher :(', 'studies :(', 'school :(',
    'exams #stressed', 'test #stressed', 'grade #stressed',
    'teacher #stressed', 'studies #stressed', 'school #stressed'
]

OTHER_QUERIES_ONE = (
    '-relationship -girlfriend -boyfriend -wife -husband '
    '-crush '

    '-work -job -project -workload -office -boss '

    '-died -"passed away" -rip -"rest in peace" '
    '-funeral -death '

    '-money -debts -salary -expenses -dollars -euros '

    '-disease -ill -hospital -sick -diagnosed '
    '-health '

    '-exams -test -grade -teacher -studies '
    '-school '

    ':('
)

OTHER_QUERIES_TWO = (
    '-relationship -girlfriend -boyfriend -wife -husband '
    '-crush '

    '-work -job -project -workload -office -boss '

    '-died -"passed away" -rip -"rest in peace" '
    '-funeral -death '

    '-money -debts -salary -expenses -dollars -euros '

    '-disease -ill -hospital -sick -diagnosed '
    '-health '

    '-exams -test -grade -teacher -studies '
    '-school '

    '#stressed'
)

OTHER_QUERIES = [OTHER_QUERIES_ONE, OTHER_QUERIES_TWO]

# tweets.delete_many({'tweet_url': {'$in': URLS}})
# tweets.update_many({"tweet_pre_classification": 'work'},
#                   {'$set': {"tweet_pre_classification": 'relationships'}})

tweets = db[db_name].tweets_raw
tweets_sample = db[db_name].tweets_raw_sample
# print("other >> " +
#       str(tweets.find({"tweet_pre_classification": 'other'}).count()))
#
# count = 0
# current_url = "blablabla"
# for document in tweets.find({"tweet_pre_classification": 'other'}):
#     myjson = json.loads(document['tweet_json_metadata'])
#     tweet = myjson['text']
#     if(
#         'exams' in tweet or 'test' in tweet or 'school' in tweet
#         or 'diploma' in tweet or 'university' in tweet or 'grade'
#         in tweet or 'teacher' in tweet or 'study' in tweet or
#         'studies' in tweet or 'studied' in tweet
#     ):
#         print(tweet)
#         print("             ")
#         current_url = document['tweet_url']
#         tweets.update_one({"tweet_url": current_url},
#                           {'$set': {
#                               "tweet_pre_classification": 'school'
#                               }})
#         count = count + 1
#
#
# print(count)
# print("other >> " +
#       str(tweets.find({"tweet_pre_classification": 'other'}).count()))

# for query in OTHER_QUERIES:
#     formatted_query = query + ' -has:videos -has:images -has:media'
#     # print(formatted_query)
#     # print(len(formatted_query))
#     try:
#         for tweet in tweepy.Cursor(api.search,
#                                    q=formatted_query,
#                                    lang="en").items(300):
#             tweet_url = "https://twitter.com/user/status/id"
#             tweet_url = tweet_url.replace("user", tweet.author.screen_name)
#             tweet_url = tweet_url.replace("id", tweet.id_str)
#             if(
#                 not hasattr(tweet, 'retweeted_status') and
#                 tweet.in_reply_to_status_id is None and
#                 tweets.find({"tweet_url": tweet_url}).count() == 0 and
#                 len(tweet.entities['urls']) == 0 and
#                 'media' not in tweet._json and (
#                     ('extended_entities' not in tweet._json) or
#                     ('extended_entities' in tweet._json and
#                      'media' not in tweet._json['extended_entities'])
#                 )
#             ):
#                 tweet_json_metadata = json.dumps(tweet._json)
#                 data = {"tweet_url": tweet_url,
#                         "tweet_pre_classification": 'other',
#                         "tweet_json_metadata": tweet_json_metadata}
#                 tweets.insert_one(data)
#                 # the lines below are for testing purposes
#                 # myjson = json.loads(tweet_json_metadata)
#                 # print(myjson['text'])
#                 # print(tweet_url)
#                 # sys.exit()
#     except tweepy.TweepError as error:
#         print(error.response.text)

CATEGORIES = ["relationships", "work", "death", "finances", "health", "school",
              "other"]
# sample size in percentage
SAMPLE_SIZE = 0.08

total_relationships = tweets.find(
    {"tweet_pre_classification": 'relationships'}
    ).count()

total_work = tweets.find(
    {"tweet_pre_classification": 'work'}
    ).count()

total_death = tweets.find(
    {"tweet_pre_classification": 'death'}
    ).count()

total_finances = tweets.find(
    {"tweet_pre_classification": 'finances'}
    ).count()

total_health = tweets.find(
    {"tweet_pre_classification": 'health'}
    ).count()

total_school = tweets.find(
    {"tweet_pre_classification": 'school'}
    ).count()

total_other = tweets.find(
    {"tweet_pre_classification": 'other'}
    ).count()

TOTAL_COUNTERS = [total_relationships, total_work, total_death, total_finances,
                  total_health, total_school, total_other]

# for t in range(0, len(TOTAL_COUNTERS)):
#     print(CATEGORIES[t] + " >>> " + str(TOTAL_COUNTERS[t]))

for t in range(0, len(TOTAL_COUNTERS)):
    print(CATEGORIES[t])
    sample_size = round(TOTAL_COUNTERS[t]*SAMPLE_SIZE)
    print(sample_size)
    sample_ids = []

    for t in tweets.find({"tweet_pre_classification": CATEGORIES[t]}):
        sample_ids.append(t["_id"])

    sample_ids_size = len(sample_ids)
    random_indexes = []

    for t in range(0, sample_size):
        random_index = random.randint(0, sample_ids_size - 1)
        while random_index in random_indexes:
            random_index = random.randint(0, sample_ids_size - 1)
        random_indexes.append(random_index)
        random_id = sample_ids[random_index]
        random_tweet = tweets.find_one({"_id": random_id})
        tweets_sample.insert_one(random_tweet)

total_relationships_sample = tweets_sample.find(
    {"tweet_pre_classification": 'relationships'}
    ).count()

total_work_sample = tweets_sample.find(
    {"tweet_pre_classification": 'work'}
    ).count()

total_death_sample = tweets_sample.find(
    {"tweet_pre_classification": 'death'}
    ).count()

total_finances_sample = tweets_sample.find(
    {"tweet_pre_classification": 'finances'}
    ).count()

total_health_sample = tweets_sample.find(
    {"tweet_pre_classification": 'health'}
    ).count()

total_school_sample = tweets_sample.find(
    {"tweet_pre_classification": 'school'}
    ).count()

total_other_sample = tweets_sample.find(
    {"tweet_pre_classification": 'other'}
    ).count()

TOTAL_COUNTERS_SAMPLE = [total_relationships_sample, total_work_sample,
                         total_death_sample, total_finances_sample,
                         total_health_sample, total_school_sample,
                         total_other_sample]

for t in range(0, len(TOTAL_COUNTERS_SAMPLE)):
    print(CATEGORIES[t] + " >>> " + str(TOTAL_COUNTERS_SAMPLE[t]))
