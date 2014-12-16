import os
import redis 
import re

app_name = "SLOTHROBOT"
redis_collection = 'txt'
redis_url = os.getenv(app_name + '_REDIS_URL', 'redis://localhost:6379')

def get_text():
    read_data = None

    with open('Thomas_Pynchon_-_Gravitys.txt', 'r') as txt:
        read_data = txt.read().decode('utf-8')

    no_space = re.sub('\W+', '', read_data).lower()

    return no_space

if __name__ == "__main__":

    r = redis.from_url(redis_url)

    text = get_text()

    r.set(redis_collection, text)
    