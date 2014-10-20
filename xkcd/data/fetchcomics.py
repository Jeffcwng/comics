__author__ = 'miguelbarbosa'
import requests
import json


def get_all_comics(start, end):  # grab all comics from 1 - 404 (because 404 is missing)
    store = []
    with open('xkcd/data/comics.json', 'w') as f:
        for n in range(start, 404):
            each_comic = requests.get("http://xkcd.com/{}/info.0.json".format(n)).json()
            store.append(each_comic)
            json.dump(each_comic, f)
        for n in range(405, end):
            each_comic = requests.get("http://xkcd.com/{}/info.0.json".format(n)).json()
            json.dump(each_comic, f)
            store.append(each_comic)
    return len(store)
