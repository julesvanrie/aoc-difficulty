import os
import json
import pickle
from datetime import datetime
from pytz import timezone
import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

from aocdifficulty.params import *


def get_leaderboard(year: int, day: int):
    """Gets the leaderboard times the first 100 contendors.
    Loads from local cache if it exists, otherwise scrapes the AOC website.
    If the leaderboard is complete, caches the data.

    Params
    ------
    year : int
        Year for which to get the leaderboard
    day : int
        Day for which to get the leaderboard

    Returns
    -------
    list, list
        Two lists, with the times for the one star and two star
    """
    eric_wastl_tz = timezone('US/Eastern')
    today = datetime.now(eric_wastl_tz)
    if not year:
        year = today.year
        if today.month != 12:
            year -= 1
    if not day:
        day = today.day
        if day > 25:
            day -= 10

    leader_path = os.path.join(DATA_PATH, str(year), f"{day}.pkl")

    # Load file if it already exists, if not, try in the temp location
    if not os.path.isfile(leader_path):
        leader_path = os.path.join(TMP_LEADERBOARD_PATH, str(year), f"{day}.pkl")
    if os.path.isfile(leader_path):
        with open(leader_path, 'rb') as file:
            data = pickle.load(file)
            return data

    print("Scraping the leaderboard")
    one_star_results, two_star_results = scrape_leaderboard(year, day)

    # If the day's leaderboard is complete, cache it locally
    if len(two_star_results) == 100:
        # Make sure the directory exists
        if not os.path.isdir(os.path.dirname(leader_path)):
            os.makedirs(os.path.dirname(leader_path))
        # Save the results
        with open(leader_path, 'wb') as file:
            pickle.dump(obj=[one_star_results, two_star_results],
                        file=file)
        print("Saved the leaderboard to cache")

    return one_star_results, two_star_results


def scrape_leaderboard(year: int, day: int):
    """Scrapes the leaderboard to get the times for the first 100 contendors

    Params
    ------
    year : int
        Year for which to get the leaderboard
    day : int
        Day for which to get the leaderboard

    Returns
    -------
    list, list
        Two lists, with the times for the one star and two star
    """
    url = f"https://adventofcode.com/{year}/leaderboard/day/{day}"
    page = requests.get(url=url).text

    # Get positions and times
    soup = BeautifulSoup(page, 'html.parser')
    positions = [int(entry.contents[0][:-1].strip())
                 for entry in soup.find_all(class_="leaderboard-position")]
    times = [entry.contents[0][-8:]
                  for entry in soup.find_all(class_="leaderboard-time")]

    # Convert times from text to minutes (float)
    times = [int(time[:2])*60 + int(time[3:5]) + int(time[6:])/60
             for time in times]

    # Split into two star and one star results
    # On the website, the two stars are shown first
    one_star_results = []
    two_star_results = []
    for i in range(0, min(100, len(positions)+1)):
        two_star_results.append(times[i])
        # If the next position is 1, then we have reached the one stars
        if positions[i+1] == 1:
            break
    # Start again to get the one star results
    # Anything remaining in times is a one star result
    start_of_one_star = len(two_star_results)
    for i in range(start_of_one_star, len(times)):
        one_star_results.append(times[i])

    return one_star_results, two_star_results


if __name__ == "__main__":
    one, two = get_leaderboard(2022, 15)
    print(len(one), len(two))
    print(one)
    print(two)
