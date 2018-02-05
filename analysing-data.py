
import configparser
from pymongo import MongoClient
import sys
import time

print("starting at " + time.strftime('%H:%M:%S', time.localtime()))

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

db_name = config.get('DB_Name', 'db')
server = config.get('DB_Server', 'server')
port = config.get('DB_Port', 'port')
username = config.get('DB_Username', 'username')
password = config.get('DB_Password', 'password')

db = MongoClient(host=server, port=int(port))
db[db_name].authenticate(username, password)

results_exp1 = db[db_name].resultant_data_exp1_raw
tweets_raw = db[db_name].tweets_raw
resultant_data_exp1 = db[db_name].resultant_data_exp1
resultant_data_exp2_part1_raw = db[db_name].resultant_data_exp2_part1_raw
input_data_exp2 = db[db_name].input_data_exp2

classification_results = {}
classification_results["death"] = 0
classification_results["finances"] = 0
classification_results["health"] = 0
classification_results["relationships"] = 0
classification_results["school"] = 0
classification_results["work"] = 0
classification_results["other"] = 0

# clusters_stress = {}
# clusters_stress["death"] = []
# clusters_stress["finances"] = []
# clusters_stress["health"] = []
# clusters_stress["relationships"] = []
# clusters_stress["school"] = []
# clusters_stress["work"] = []
# clusters_stress["other"] = []

clusters_stress = {}
clusters_stress["death"] = {}
clusters_stress["death"]["useful"] = 0
clusters_stress["death"]["useless"] = 0
clusters_stress["death"]["ad"] = 0
clusters_stress["death"]["cc"] = 0
clusters_stress["death"]["ges"] = 0
clusters_stress["death"]["sm"] = 0
clusters_stress["death"]["ss"] = 0

clusters_stress["finances"] = {}
clusters_stress["finances"]["useful"] = 0
clusters_stress["finances"]["useless"] = 0
clusters_stress["finances"]["ad"] = 0
clusters_stress["finances"]["cc"] = 0
clusters_stress["finances"]["ges"] = 0
clusters_stress["finances"]["sm"] = 0
clusters_stress["finances"]["ss"] = 0

clusters_stress["health"] = {}
clusters_stress["health"]["useful"] = 0
clusters_stress["health"]["useless"] = 0
clusters_stress["health"]["ad"] = 0
clusters_stress["health"]["cc"] = 0
clusters_stress["health"]["ges"] = 0
clusters_stress["health"]["sm"] = 0
clusters_stress["health"]["ss"] = 0

clusters_stress["relationships"] = {}
clusters_stress["relationships"]["useful"] = 0
clusters_stress["relationships"]["useless"] = 0
clusters_stress["relationships"]["ad"] = 0
clusters_stress["relationships"]["cc"] = 0
clusters_stress["relationships"]["ges"] = 0
clusters_stress["relationships"]["sm"] = 0
clusters_stress["relationships"]["ss"] = 0

clusters_stress["school"] = {}
clusters_stress["school"]["useful"] = 0
clusters_stress["school"]["useless"] = 0
clusters_stress["school"]["ad"] = 0
clusters_stress["school"]["cc"] = 0
clusters_stress["school"]["ges"] = 0
clusters_stress["school"]["sm"] = 0
clusters_stress["school"]["ss"] = 0

clusters_stress["work"] = {}
clusters_stress["work"]["useful"] = 0
clusters_stress["work"]["useless"] = 0
clusters_stress["work"]["ad"] = 0
clusters_stress["work"]["cc"] = 0
clusters_stress["work"]["ges"] = 0
clusters_stress["work"]["sm"] = 0
clusters_stress["work"]["ss"] = 0

WORKERS_PER_TWEETS = 3

usefull_tweets = 0
checked_urls = []

for result_exp2_part1 in resultant_data_exp2_part1_raw.find():
    input_data = input_data_exp2.find_one(
        {"tweet_url": result_exp2_part1["tweet_url"]})
    if result_exp2_part1["available_and_readable?"] == "yes":
            clusters_stress[
                input_data["tweet_classification"]
            ]["useful"] = clusters_stress[
                input_data["tweet_classification"]
                ]["useful"] + 1
            clusters_stress[
                input_data["tweet_classification"]
            ][result_exp2_part1["tweet_support_strategy"]] = clusters_stress[
                input_data["tweet_classification"]
                ][result_exp2_part1["tweet_support_strategy"]] + 1
    else:
            clusters_stress[
                input_data["tweet_classification"]
            ]["useless"] = clusters_stress[
                input_data["tweet_classification"]
                ]["useless"] + 1

for c in clusters_stress:
    print(c)
    print(clusters_stress[c])
    print("=====================")

# def readable_and_stressful_tweet(answers):
#     return all(x == answers[0] for x in answers) and answers[0] == "yes"
#
#
# def useful_tweet(answers):
#     return all(x == answers[0] for x in answers)
#
# for result in results_exp1.find():
#     url = result['tweet_url']
#     # print("usefull tweets: " + str(usefull_tweets))
#     count = results_exp1.find({"tweet_url": url}).count()
#     if (count == WORKERS_PER_TWEETS and url not in checked_urls):
#         checked_urls.append(url)
#         q1_answers = []
#         q2_answers = []
#         q3_answers = []
#         q4_answers = []
#
#         for r in results_exp1.find({"tweet_url": url}):
#             q1_answers.append(r["available_and_readable?"])
#             q2_answers.append(r["stressful_situation?"])
#             q3_answers.append(r["tweet_classification"])
#             q4_answers.append(r["tweet_classification_other"])
#
#         if(
#             readable_and_stressful_tweet(q1_answers) and
#             readable_and_stressful_tweet(q2_answers) and
#             useful_tweet(q3_answers)
#         ):
#             usefull_tweets = usefull_tweets + 1
#             classification_results[q3_answers[0]] = classification_results[
#                 q3_answers[0]] + 1
#             clusters_stress[q3_answers[0]].append(url)
#
#
# print("Usefull tweets: " + str(usefull_tweets))
# print("Classifications: " + str(classification_results))
# print("death: "+str(len(clusters_stress["death"])))
# print("finances: "+str(len(clusters_stress["finances"])))
# print("health: "+str(len(clusters_stress["health"])))
# print("relationships: "+str(len(clusters_stress["relationships"])))
# print("school: "+str(len(clusters_stress["school"])))
# print("work: "+str(len(clusters_stress["work"])))
# print("other: "+str(len(clusters_stress["other"])))
#
# print("===========================")
#
# for cluster in clusters_stress:
#     total_raw_tweets_cluster = tweets_raw.find(
#         {"tweet_pre_classification": cluster})
#     total_useful = 0
#     for t in total_raw_tweets_cluster:
#         if(
#             t['tweet_url'] in clusters_stress["death"] or
#             t['tweet_url'] in clusters_stress["finances"] or
#             t['tweet_url'] in clusters_stress["health"] or
#             t['tweet_url'] in clusters_stress["relationships"] or
#             t['tweet_url'] in clusters_stress["school"] or
#             t['tweet_url'] in clusters_stress["work"] or
#             t['tweet_url'] in clusters_stress["other"]
#         ):
#             total_useful = total_useful + 1
#             tweet_classification = ""
#             if (t['tweet_url'] in clusters_stress["death"]):
#                 tweet_classification = "death"
#             elif (t['tweet_url'] in clusters_stress["finances"]):
#                 tweet_classification = "finances"
#             elif (t['tweet_url'] in clusters_stress["health"]):
#                 tweet_classification = "health"
#             elif (t['tweet_url'] in clusters_stress["relationships"]):
#                 tweet_classification = "relationships"
#             elif (t['tweet_url'] in clusters_stress["relationships"]):
#                 tweet_classification = "relationships"
#             elif (t['tweet_url'] in clusters_stress["school"]):
#                 tweet_classification = "school"
#             elif (t['tweet_url'] in clusters_stress["work"]):
#                 tweet_classification = "work"
#             else:
#                 tweet_classification = "other"
#
#             data = {"tweet_url": t['tweet_url'],
#                     "tweet_classification": tweet_classification}
#
#             resultant_data_exp1.insert_one(data)
#     hits = 0
#     for t in tweets_raw.find({"tweet_pre_classification": cluster}):
#         if t['tweet_url'] in clusters_stress[cluster]:
#             hits = hits + 1
#     accuracy_percentage = (hits * 100) / total_useful
#     message = (
#         str(round(accuracy_percentage, 2))+"% of the tweets classified as '"
# +
#         cluster+"'"" by the keywords approach were also put in the same "
#         "category by the"
#         " participants. In absolute numbers: "+str(hits)+" from a total of"
#         " "+str(total_useful)+" tweets."
#     )
#     print(message)
#
# print("===========================")
print("finishing at " + time.strftime('%H:%M:%S', time.localtime()))
