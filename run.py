from twython import Twython
import os
import redis 
import random

app_name = "SLOTHROBOT"
redis_collection = 'txt'

consumer_key = os.environ.get(app_name + '_CONSUMER_KEY')
consumer_secret = os.environ.get(app_name + '_CONSUMER_SECRET')
access_token = os.environ.get(app_name + '_ACCESS_TOKEN')
access_token_secret = os.environ.get(app_name + '_ACCESS_TOKEN_SECRET')

redis_url = os.getenv(app_name + '_REDIS_URL', 'redis://localhost:6379')

def get_start(text):
    return random.randint(0, max(len(text) - 140, 0))

if __name__ == "__main__":

    r = redis.from_url(redis_url)
    
    twitter = Twython(consumer_key,
                  consumer_secret,
                  access_token,
                  access_token_secret)


    # Get our full text from db
    text = r.get(redis_collection)

    print "%s characters left" % len(text)

    # Find a random 140 character range
    start = get_start(text)
    end = start + 140

    print "Start: %s, End: %s" % (start, end)

    # Extract the tweet, and remove it from the text
    tweet = text[start:end]
    text = text[:start] + text[end:]

    print tweet

    # Send to twitter
    twitter.update_status(status=tweet)

    # Save in DB
    r.set(redis_collection, text)