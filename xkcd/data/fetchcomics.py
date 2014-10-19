__author__ = 'miguelbarbosa'
import requests
import json
import glob


def get_all_comics_part_1():  # grab all comics from 1 - 404 (because 404 is missing)
    with open('xkcd/data/part1.json', 'w') as f:
        for n in range(1, 404):
            each_comic = requests.get("http://xkcd.com/{}/info.0.json".format(n)).json()
            json.dump(each_comic, f)


def get_all_comics_part_2():  # grab all comics from 405 - current date
    latest_comic = requests.get("http://xkcd.com/info.0.json").json()
    with open('xkcd/data/part2.json', 'w') as f:
        for n in range(405, latest_comic['num'] + 1):
            each_comic = requests.get("http://xkcd.com/{}/info.0.json".format(n)).json()
            json.dump(each_comic, f)


def add_both_files():  # combine both files
    read_files = glob.glob("xkcd/data/*.json")
    with open("xkcd_allcomics.json", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
