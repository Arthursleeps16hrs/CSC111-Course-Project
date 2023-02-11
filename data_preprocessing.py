"""CSC111 Winter 2021 Final Project Part 1: Data pre-processing

Instructions
===============================

This Python module reads .json data files about users' reviews of games
on steam and the some game data on steam. It filters out messy data and
transform data into python build-in data type.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Yanke Mao, Yiteng Sun, Weiheng Wang and Jiaxu Li.
"""

####################################################################################################
# Part 1: load .json files and pre-processing data
####################################################################################################

import json
import python_ta


def open_user_review(file_name: str) -> list[dict]:
    """
    Read the data file 'australian_user_reviews.json'.
    Load the review data and transform it into list[dict].
    Each element in the list is the review data from one user.
    And we drop some data with extremely messy strings.
    """
    with open(file_name, encoding="utf-8") as f:
        s = f.read()
        # avoid JSONDecodeError when calling json.loads
        s = s.replace('\'', '\"')
        s = s.replace('True', '\"True\"')
        s = s.replace('False', '\"False\"')
        # using s.split("\n") to divide review data from each user
        data = s.split("\n")
        data_so_far = []
        for x in data:
            try:
                # for each user, we drop their detailed comments to avoid JSONDecodeError.
                # Since there are lots of messy strings in detailed comments.
                s = x.split('\"reviews\": ')[1][:-2]
                s = s.split('\"funny\": \"\", ')
                h = ['{' + m for m in s[1:]]
                reviews_so_far = []
                for y in h:
                    j = y.split(', \"review\":')[0] + '}'
                    reviews_so_far.append(json.loads(j))
                # reviews_so_far is a clean list of the user's reviews of games,
                # in which we drop user's detailed comments.
                i = x.split(', \"reviews\":')[0] + '}'
                user_data = json.loads(i)
                # i is the information of user's account.
                user_data['reviews'] = reviews_so_far
                data_so_far.append(user_data)
            except (json.decoder.JSONDecodeError, IndexError):
                # we drop the data with extremely messy strings to avoid JSONDecodeError
                pass

    return data_so_far


def open_steam_games(file_name: str) -> list[dict]:
    """
    Read the data file 'steam_games.json'.
    Load the games' data and transform it into list[dict].
    Each element in the list is the data of one game.
    And we drop some data with extremely messy strings.
    """
    with open(file_name, encoding="utf-8") as f:
        s = f.read()
        # avoid JSONDecodeError when calling json.loads
        s = s.replace('u\'', '\"')
        s = s.replace('\'', '\"')
        s = s.replace('True', '\"True\"')
        s = s.replace('False', '\"False\"')
        # using s.split("\n") to divide data of each game
        data = s.split("\n")
        data_so_far = []

        for x in data:
            try:
                data_so_far.append(json.loads(x))
            except json.decoder.JSONDecodeError:
                # we drop the data with extremely messy strings to avoid JSONDecodeError
                pass
            else:
                pass

    return data_so_far


def filter_the_reviews_data(file_name: str) -> dict:
    """the function that filter the reviews data

    this file format is {'user_id': ([{'item_id': 'recommend'},...], 'user_url')}
    """
    single_data = {}
    data = open_user_review(file_name)
    for item in data:
        single_data[item['user_id']] = ([{x['item_id']: x['recommend']} for x in item['reviews']],
                                        item['user_url'])

    return single_data


def filter_the_games_data(file_name: str) -> dict:
    """the function

    the file format is {'id': ('app_name', 'url')}
    """
    dictionary = {}
    data = open_steam_games(file_name)
    for item in data:
        if 'id' in item:
            if 'title' in item:
                dictionary[item['id']] = (item['title'], item['url'])
            elif 'app_name' in item:
                dictionary[item['id']] = (item['app_name'], item['url'])
            else:
                dictionary[item['id']] = ('N/A', item['url'])
        else:
            pass
    return dictionary


python_ta.check_all(config={
    'extra-imports': ['json', 'math', 'tkinter', 'tkinter.messagebox'],
    # the names (strs) of imported modules
    'allowed-io': ['open_steam_games', 'open_user_review'],
    # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['E1136']
})
