"""CSC111 Winter 2021 Final Project: Recommendation of games/game friends

Instructions
===============================

This Python module is the main part of our project. In this project, we're going to
construct an interface for users to do recommendation on games/game friends.
User can freely choose to obtain a recommendation on games or on game friends.
With the input user id/favorite game's name, users can gain their unique recommendation.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Yanke Mao, Yiteng Sun, Weiheng Wang and Jiaxu Li.
"""

####################################################################################################
# Main Part: load data sets and call functions to do recommendation
####################################################################################################

import computation
import interface


recommendation_graph = computation.load_weighted_graph('australian_user_reviews.json',
                                                       'steam_games.json')
interface.recommend_interface(recommendation_graph)
