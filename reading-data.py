
import configparser
from pymongo import MongoClient
import csv
import sys

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

resultant_data_exp1 = db[db_name].resultant_data_exp1
results = db[db_name].resultant_data_exp2_part2_raw
input_data_exp3 = db[db_name].input_data_exp3
# You must have such a .csv file in your project folder.
FILE_NAME = "results-exp3.csv"

# Fields provided by Amazon MTurk. They are here just for checking purposes.
FIELD_NAMES = [
    "HITId", "HITTypeId", "Title", "Description",
    "Keywords", "Reward", "CreationTime", "MaxAssignments",
    "RequesterAnnotation", "AssignmentDurationInSeconds",
    "AutoApprovalDelayInSeconds", "Expiration", "NumberOfSimilarHITs",
    "LifetimeInSeconds", "AssignmentId", "WorkerId",
    "AssignmentStatus", "AcceptTime", "SubmitTime",
    "AutoApprovalTime", "ApprovalTime", "RejectionTime",
    "RequesterFeedback", "WorkTimeInSeconds", "LifetimeApprovalRate",
    "Last30DaysApprovalRate", "Last7DaysApprovalRate",
    "Input.tweet_url", "Answer.Q1Answer", "Answer.Q2Answer", "Answer.Q3Answer",
    "Answer.Q4Answer", "Approve", "Reject"
]

# Experiment 1 (experiment1-mturk.html)
# with open(FILE_NAME, newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         if (row['AssignmentStatus'] == 'Approved'):
#             data = {"tweet_url": row['Input.tweet_url'],
#                     "available_and_readable?": row['Answer.Q1Answer'],
#                     "stressful_situation?": row['Answer.Q2Answer'],
#                     "tweet_classification": row['Answer.Q3Answer'],
#                     "tweet_classification_other": row['Answer.Q4Answer']}
#             results.insert_one(data)

# Experiment 2 part 1 (experiment2-mturk.html)
# with open(FILE_NAME, newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         if (row['AssignmentStatus'] == 'Approved'):
#             data = {"tweet_url": row['Input.tweet_url'],
#                     "available_and_readable?": row['Answer.Q1Answer'],
#                     "tweet_support_message": row['Answer.Q2Answer']}
#             results.insert_one(data)

# Experiment 3 (experiment4-mturk.html)
clusters_stress = {}
clusters_stress["death"] = {}
clusters_stress["death"]["total"] = 0
clusters_stress["death"]["none"] = 0
clusters_stress["death"]["ad"] = 0
clusters_stress["death"]["cc"] = 0
clusters_stress["death"]["ges"] = 0
clusters_stress["death"]["sm"] = 0
clusters_stress["death"]["ss"] = 0

clusters_stress["finances"] = {}
clusters_stress["finances"]["total"] = 0
clusters_stress["finances"]["none"] = 0
clusters_stress["finances"]["ad"] = 0
clusters_stress["finances"]["cc"] = 0
clusters_stress["finances"]["ges"] = 0
clusters_stress["finances"]["sm"] = 0
clusters_stress["finances"]["ss"] = 0

clusters_stress["health"] = {}
clusters_stress["health"]["total"] = 0
clusters_stress["health"]["none"] = 0
clusters_stress["health"]["ad"] = 0
clusters_stress["health"]["cc"] = 0
clusters_stress["health"]["ges"] = 0
clusters_stress["health"]["sm"] = 0
clusters_stress["health"]["ss"] = 0

clusters_stress["relationships"] = {}
clusters_stress["relationships"]["total"] = 0
clusters_stress["relationships"]["none"] = 0
clusters_stress["relationships"]["ad"] = 0
clusters_stress["relationships"]["cc"] = 0
clusters_stress["relationships"]["ges"] = 0
clusters_stress["relationships"]["sm"] = 0
clusters_stress["relationships"]["ss"] = 0

clusters_stress["school"] = {}
clusters_stress["school"]["total"] = 0
clusters_stress["school"]["none"] = 0
clusters_stress["school"]["ad"] = 0
clusters_stress["school"]["cc"] = 0
clusters_stress["school"]["ges"] = 0
clusters_stress["school"]["sm"] = 0
clusters_stress["school"]["ss"] = 0

clusters_stress["work"] = {}
clusters_stress["work"]["total"] = 0
clusters_stress["work"]["none"] = 0
clusters_stress["work"]["ad"] = 0
clusters_stress["work"]["cc"] = 0
clusters_stress["work"]["ges"] = 0
clusters_stress["work"]["sm"] = 0
clusters_stress["work"]["ss"] = 0

with open(FILE_NAME, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        if (row['Answer.Q1Answer'] == 'yes'):
            # print("-----------")
            stressful_situation = resultant_data_exp1.find_one(
                {"tweet_url": row['Input.tweet_url']})
            # print(stressful_situation["tweet_classification"])
            # print(row['Answer.Q3Answer'])
            # print(row['Answer.Q2Answer'])
            # print("-----------")
            clusters_stress[
                stressful_situation["tweet_classification"]
                ]["total"] = clusters_stress[
                    stressful_situation["tweet_classification"]
                ]["total"] + 1
            full_answer = row['Answer.Q3Answer'] + row['Answer.Q2Answer']
            if (len(full_answer) > 0):
                if (row['Answer.Q3Answer'] == 'ges'):
                    clusters_stress[
                        stressful_situation["tweet_classification"]
                        ]["ges"] = clusters_stress[
                            stressful_situation["tweet_classification"]
                        ]["ges"] + 1
                if (row['Answer.Q2Answer'].find('|') != -1):
                    q2 = row['Answer.Q2Answer'].split('|')
                    for support in q2:
                        clusters_stress[
                            stressful_situation["tweet_classification"]
                            ][support] = clusters_stress[
                                stressful_situation["tweet_classification"]
                            ][support] + 1
                else:
                    if (len(row['Answer.Q2Answer']) > 0):
                        support = row['Answer.Q2Answer']
                        clusters_stress[
                            stressful_situation["tweet_classification"]
                            ][support] = clusters_stress[
                                stressful_situation["tweet_classification"]
                            ][support] + 1
            else:
                clusters_stress[
                    stressful_situation["tweet_classification"]
                    ]["none"] = clusters_stress[
                        stressful_situation["tweet_classification"]
                    ]["none"] + 1
            # for c in clusters_stress:
            #     print(c + ": "+str(clusters_stress[c]))
            # print("         ")
            # print("         ")
for c in clusters_stress:
    print(c)
    print(clusters_stress[c])
    print("         ")
    #         print(row['Input.tweet_url'])
    #         print("Answers: Q2-("+row[
    #             'Answer.Q2Answer']+"), Q3-("+row['Answer.Q3Answer']+")")
    #         print("         ")
    #         count = count + 1
    # print(count)

# for result in results.find():
#     if result['available_and_readable?'] == 'yes':
#         data = {"tweet_url": result["tweet_url"],
#                 "tweet_support_message": result["tweet_support_message"]}
#         input_data_exp3.insert_one(data)
