__author__ = 'miguelbarbosa'
import random
import requests


def get_random_comic():
    latest_comic = requests.get("http://xkcd.com/info.0.json").json()
    random_num = random.randint(1, latest_comic['num'])
    random_comic = requests.get("http://xkcd.com/{}/info.0.json".format(random_num)).json()
    return random_comic
