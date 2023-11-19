import os
import json
import pickle
from datetime import datetime
import requests
import numpy as np
import pandas as pd

from aocdifficulty.scraper import get_leaderboard

json_url = "https://raw.githubusercontent.com/topaz/aoc-tmp-stats/master/aoc-2015-2021-stats.json"

data_dir = "data"
json_path = os.path.join(data_dir, "history.json")


def first_100_history() -> (pd.DataFrame, pd.DataFrame):
    df_one = make_history_df(1)
    df_two = make_history_df(2)
    last_year = df_one.index.get_level_values(0).max()
    for year in range(last_year+1, datetime.today().year):
        new_one, new_two = load_leaderboards(year)
        df_one = pd.concat([df_one, new_one])
        df_two = pd.concat([df_two, new_two])

    return df_one, df_two

def make_history_df(level: int) -> pd.DataFrame:
    """Makes a dataframe from the history json containing the times of the
    first 100 contenders for every day of every year

    Parameters
    ----------
    level : int
        Level for which to make the DataFrame. One of [1, 2]

    Returns
    -------
    pd.DataFrame
        Dataframe with for every day for every year the times
    """
    history = load_history_json()
    df = pd.DataFrame()
    df = pd.concat([
        pd.Series([
            history[str(year)][str(day)][str(level)][n] / 60
            for day in range(1,26)
            for year in range(2015, 2022)
            ], name=n)
        for n in range(1,101)
    ], axis=1)

    df['year'] = [year
                  for day in range(1,26)
                  for year in range(2015, 2022)]
    df['day'] = [day
                 for day in range(1,26)
                 for year in range(2015, 2022)]
    df = df.set_index(['year','day'])

    return df


def load_history_json() -> dict:
    """Loads Eric Wastl's json with historical times in seconds from GitHub
    Gets it from local storage if it exists. Else first saves it locally.

    Returns
    -------
    dict
        The json data (year > day > level > contendor)
    """
    if not os.path.isfile(json_path):
        json_data = requests.get(json_url).text
        print("Fetched the json from GitHub")

        with open(json_path, 'w') as file:
            file.write(json_data)
    else:
        print("Using cached json")

    with open(json_path) as file:
        history = json.load(file)

    return history


def fetch_leaderboards(year: int):
    """Return a dataframe with the leaderboard times (100) for a year

    Parameters
    ----------
    year : int
        Year for which to get the data
    """
    data_one = []
    data_two = []
    for day in range(1,26):
        print(f"Scraping day {day}")
        board_one, board_two = get_leaderboard(year, day)
        data_one.append(board_one)
        data_two.append(board_two)

    df_one = pd.DataFrame(data_one, index=range(1,26), columns=range(1,101))
    df_two = pd.DataFrame(data_two, index=range(1,26), columns=range(1,101))

    return df_one, df_two


def load_leaderboards(year: int):
    """Return a dataframe with the leaderboard times (100) for a year
    Loads leaderboard from cache if it exists. Otherwise gets it from the website.
    Parameters
    ----------
    year : int
        Year for which to get the data
    """
    leader_path = os.path.join(data_dir, f"{year}.pkl")

    if not os.path.isfile(leader_path):
        print(f"Scraping the leaderboards for year {year}")
        df_one, df_two = fetch_leaderboards(year)
        with open(leader_path, 'wb') as file:
            pickle.dump(obj=[df_one, df_two], file=file)

    else:
        print("Using cached data")
        with open(leader_path, 'rb') as file:
            data = pickle.load(file)
            df_one, df_two = data

    # Set multilevel index with year and day
    df_one['year'] = year
    df_one['day'] = range(1,26)
    df_one = df_one.set_index(['year','day'])
    df_two['year'] = year
    df_two['day'] = range(1,26)
    df_two = df_two.set_index(['year','day'])

    return df_one, df_two


if __name__ == "__main__":
    # print(load_history_json()['2015']['1']['1'])
    # print(load_leaderboards(2022))
    print(first_100_history())
