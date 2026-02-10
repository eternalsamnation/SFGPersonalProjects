import json
import pandas as pd

ACCOUNT = 'wowgodsamit'

def extract_insta_data():
    following = []
    followers = []

    with open(f'./InstagramData/{ACCOUNT}/connections/followers_and_following/following.json', 'r') as file:
        following_data = json.load(file)

    for i in following_data['relationships_following']:
        following.append(i['string_list_data'][0]['value'])

    with open(f'./InstagramData/{ACCOUNT}/connections/followers_and_following/followers_1.json', 'r') as file:
        followers_data = json.load(file)

    for i in followers_data:
        followers.append(i['string_list_data'][0]['value'])

    followers.sort()
    following.sort()

    followers_for_df = followers + ['NA']*(len(following)-len(followers))

    df = pd.DataFrame({'followers':followers_for_df,'following':following})
    df.to_csv(f'./InstagramData/Instagram{ACCOUNT}_followers.csv',index=False)