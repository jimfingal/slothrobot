from twython import Twython
import os
import redis 
import re
import random
import time

app_name = "SLOTHROBOT"
redis_collection = 'txt'

consumer_key = os.environ.get(app_name + '_CONSUMER_KEY')
consumer_secret = os.environ.get(app_name + '_CONSUMER_SECRET')
access_token = os.environ.get(app_name + '_ACCESS_TOKEN')
access_token_secret = os.environ.get(app_name + '_ACCESS_TOKEN_SECRET')

def write_tweet(tweet):
    twitter.update_status(status=tweet)
    return True


def get_text():
    read_data = None

    with open('Thomas_Pynchon_-_Gravitys.txt', 'r') as txt:
        read_data = txt.read().decode('utf-8')

    no_space = re.sub('\W+', '', read_data).lower()

    return no_space


def get_start(text):
    return random.randint(0, max(len(text) - 140, 0))

def get_random_140(text):
    start = get_start(text)
    return text[start:start + 140]


def run_tweet(r, twitter):
    remaining_text = r.get(redis_collection)

    if not remaining_text:
        print "getting new text"
        remaining_text = get_text()

    print "%s characters left" % len(remaining_text)

    # End bot when < 140 char
    if len(remaining_text) > 140:

        start = get_start(remaining_text)
        end = start + 140

        print "Start: %s, End: %s" % (start, end)

        tweet = remaining_text[start:end]

        remaining_text = remaining_text[:start] + remaining_text[end:]

        print tweet
        twitter.update_status(status=tweet)
        
        r.set(redis_collection, remaining_text)


if __name__ == "__main__":
    redis_url = os.getenv(app_name + '_REDIS_URL', 'redis://localhost:6379')

    r = redis.from_url(redis_url)
    
    print consumer_key
    print consumer_secret
    print access_token
    print access_token_secret
    twitter = Twython(consumer_key,
                  consumer_secret,
                  access_token,
                  access_token_secret)

    while True:
        run_tweet(r, twitter)
        time.sleep(120)

    
