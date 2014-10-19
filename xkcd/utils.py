__author__ = 'miguelbarbosa'
import random
import requests
import json
import glob


def get_random_comic():
    latest_comic = requests.get("http://xkcd.com/info.0.json").json()
    random_num = random.randint(1, latest_comic['num'])
    random_comic = requests.get("http://xkcd.com/{}/info.0.json".format(random_num)).json()
    return random_comic


def get_all_comics_part_1():  # grab all comics from 1 - 404 (because 404 is missing)
    latest_comic = requests.get("http://xkcd.com/info.0.json").json()
    with open('comics/xkcd/data/part1.txt', 'w') as f:
        for n in range(1, 404):
            each_comic = requests.get("http://xkcd.com/{}/info.0.json".format(n)).json()
            json.dump(each_comic, f)
    return latest_comic


def get_all_comics_part_2():  # grab all comics from 405 - current date
    latest_comic = requests.get("http://xkcd.com/info.0.json").json()
    with open('comics/xkcd/data/part2.txt', 'w') as f:
        for n in range(405, latest_comic['num'] + 1):
            each_comic = requests.get("http://xkcd.com/{}/info.0.json".format(n)).json()
            json.dump(each_comic, f)
    return latest_comic


def add_both_files():  # combine both files
    read_files = glob.glob("comics/xkcd/data/*.txt")
    with open("xkcd_allcomics.json", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
