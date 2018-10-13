from config import TWITTER_API_KEY, TWITTER_API_SECRET_KEY
import db

import base64
import requests
import json
import pprint
import time

def get_credentials():
    return '{}:{}'.format(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)

def encode_base64(s):
    return base64.b64encode(s.encode('utf-8'))

def get_bearer_token():
    token = encode_base64(get_credentials()).decode('ascii')
    r = requests.post('https://api.twitter.com/oauth2/token',
                    headers={
                        'Authorization': 'Basic {}'.format(token),
                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                    },
                    data='grant_type=client_credentials'
    )

    r = r.json()
    assert r['token_type'] == 'bearer'
    return 'Bearer ' + r['access_token']

def parse_tweets(json):
    tweets = {}
    for tweet in json['statuses']:
        tweets[tweet['id']] = {
            'text': tweet['text'],
            'created': tweet['created_at'],
            'rt_count': tweet['retweet_count'],
            'fav_count': tweet['favorite_count']
        }

    return tweets

def search(query, n, result_type):
    assert n > 0 and n <= 100
    assert result_type == 'recent' or result_type == 'mixed' or result_type == 'popular'

    params = {'q': query, 'result_type': result_type, 'count': str(n), 'lang': 'en'}
    r = requests.get('https://api.twitter.com/1.1/search/tweets.json',
                     params=params,
                     headers={
                         'User-Agent': 'Augury MHacks',
                         'Authorization': get_bearer_token()
                     }
    )

    return parse_tweets(r.json())

def save_in_db(tweets):
    for tweet in tweets:
        t_id = tweet
        tweet = tweets[tweet]
        db.insert(t_id, tweet['text'], tweet['created'], tweet['rt_count'], tweet['fav_count'])

def main():
    tweets = search('"tesla" OR "Tesla" -filter:retweets', 100, 'recent')
    pprint.pprint(tweets)
    save_in_db(tweets)

    tweets = search('"tesla" OR "Tesla" -filter:retweets', 100, 'popular')
    pprint.pprint(tweets)
    save_in_db(tweets)

    time.sleep(4)

while True:
    main()
