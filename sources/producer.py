import os

import tweepy
from confluent_kafka import Producer


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


topic = 'test-topic'
p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

track = ['python',]


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # print(status)
        print(status.text)
        p.produce(topic, status.text)
        p.flush()


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(
    auth=api.auth,
    listener=myStreamListener
)

myStream.filter(track=track)
