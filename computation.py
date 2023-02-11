"""CSC111 Winter 2021 Final Project Part 2: Computation

Instructions
===============================

This Python module defines two new Classes, which are _ReviewVertex and GameRecommendationGraph.
The data about users, games, and reviews that was pre-processed in part 1
will be stored in the GameRecommendationGraph class. We are going to
calculate the similarity scores between objects and recommend games and game friends with
higher similarity scores to users.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Yanke Mao, Yiteng Sun, Weiheng Wang and Jiaxu Li.
"""


###################################################################################################
# Part 2: Construct the Graph to store data about users, reviews, and games.
# Using simularity scores to do recommendation for game friends and games.
###################################################################################################

from __future__ import annotations
from typing import Any, Union
import math
import python_ta
import data_preprocessing


class _ReviewVertex:
    """A vertex in our game recommendation graph, which can represent a user or a game.

    Each vertex item is either a user id or game title. Both are represented as strings.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or a game.
        - kind: The type of this vertex: 'user' or 'game'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'game'}

    """
    item: Any
    kind: str
    url: str
    neighbours: dict[_ReviewVertex, Union[int, float]]

    def __init__(self, item: Any, kind: str, url: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'game'}
        """
        self.item = item
        self.kind = kind
        self.url = url
        self.neighbours = {}

    def get_url(self) -> str:
        """get the url page of one single game or one single user
        """
        return self.url

    def get_consice_similarity(self, other: _ReviewVertex) -> float:
        """the function that can help to get the consice similarity of two users.

        """
        user1 = []
        user2 = []
        for item in self.neighbours:
            if item in other.neighbours:
                user1.append(self.neighbours[item])
                user2.append(other.neighbours[item])
            else:
                user1.append(self.neighbours[item])
                user2.append('N/A')

        for item in other.neighbours:
            if item not in self.neighbours:
                user1.append('N/A')
                user2.append(other.neighbours[item])

        return consice_similarity(user1, user2)


class GameRecommendationGraph:
    """A graph that used to represent a game review networks and contains the ratings to each games.

    """
    _vertices: dict[Any, _ReviewVertex]

    def __init__(self) -> None:
        """Initialize a new empty game recommendation graph.
        """
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str, url: str) -> None:
        """Add a new vertex in this graph.

        Preconditions:
            - kind in {'user', 'game'}
        """
        if item not in self._vertices:
            self._vertices[item] = _ReviewVertex(item, kind, url)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float]) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'game'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    ################################################################################################
    # the following codes are our main body of the graph
    ################################################################################################

    def get_two_items_similarity_score(self, item1: Any, item2: Any) -> float:
        """get the similarity score of two items.

        test for this function: self.get_two_items_similarity_score('DJKamBer', '76561198077246154')
        """
        if item1 in self._vertices and item2 in self._vertices:
            return self._vertices[item1].get_consice_similarity(self._vertices[item2])
        else:
            raise ValueError

    def find_similar_player(self, player: Any, limit: int) -> Any:
        """find players that has similar ratings to the given player

        Preconditions:
            - player in self._vertices
            - self._vertices[player].kind == 'user'
            - limit >= 1

        """
        if player not in self._vertices:
            return 'out of range'

        users = self.get_all_vertices(kind='user')
        users_score = [(x, self.get_two_items_similarity_score(x, player))
                       for x in users if x != player]

        s1 = sorted(users_score, key=lambda x: x[0], reverse=True)
        s2 = sorted(s1, key=lambda x: x[1], reverse=True)
        result_so_far = []
        for i in range(0, limit):
            if s2[i][1] == 0:
                pass
            else:
                result_so_far.append(s2[i][0])

        if len(result_so_far) == 0:
            return 'No recommended friends'
        else:
            return [(user, self._vertices[user].get_url()) for user in result_so_far]

    def recommend_games(self, game: str, limit: int) -> Union[list[tuple[str, str]], str]:
        """this function can help to recommend the games that satisfies your favorite.

        Preconditions:
            - game in self._vertices
            - self._vertices[game].kind == 'game'
            - limit >= 1

        """
        if game not in self._vertices:
            return 'out of range'

        games = self.get_all_vertices(kind='game')
        games_scores = [(x, self.get_two_items_similarity_score(x, game))
                        for x in games if x != game]

        s1 = sorted(games_scores, key=lambda x: x[0], reverse=True)
        s2 = sorted(s1, key=lambda x: x[1], reverse=True)

        recommend_so_far = []
        for i in range(0, limit):
            if s2[i][1] == 0:
                pass
            else:
                recommend_so_far.append(s2[i][0])

        if len(recommend_so_far) == 0:
            return 'No recommended games'
        else:
            return [(game_id, self._vertices[game_id].url) for game_id in recommend_so_far]


####################################################################################################
# the following functions are given to prepare the environment for the above graph
####################################################################################################


def load_weighted_graph(reviews_file: str, game_names_file: str) -> GameRecommendationGraph:
    """Return a game recommendation WEIGHTED graph corresponding to the given datasets.

    try the following code to test this function:
    load_weighted_graph('json/example_user_reviews.json', 'steam_games.json')
    load_weighted_graph('australian_user_reviews.json', 'steam_games.json')

    format of game_files: {'id': ('app_name', 'url')}
    format of user_files: {'user_id': ([{'item_id': 'recommend'},...], 'user_url')}
    """
    user_files = data_preprocessing.filter_the_reviews_data(reviews_file)
    game_files = data_preprocessing.filter_the_games_data(game_names_file)

    graph = GameRecommendationGraph()

    for user_id in user_files:
        graph.add_vertex(item=user_id, kind='user', url=user_files[user_id][1])

        for review in user_files[user_id][0]:
            key = list(review.keys())[0]
            if key in game_files and review[key] == 'True':
                graph.add_vertex(game_files[key][0], 'game', game_files[key][1])
                graph.add_edge(user_id, game_files[key][0], weight=1)
            if key in game_files and review[key] == 'False':
                graph.add_vertex(game_files[key][0], 'game', game_files[key][1])
                graph.add_edge(user_id, game_files[key][0], weight=0)

    return graph


def consice_similarity(user1: list, user2: list) -> float:
    """
    compute the consice similarity of two users.
    >>> u1 = [4, 'N/A', 'N/A', 5, 1, 'N/A', 'N/A']
    >>> u2 = [5, 5, 4, 'N/A', 'N/A', 'N/A', 'N/A']
    >>> u3 = ['N/A', 'N/A', 'N/A', 2, 4, 5, 'N/A']
    >>> consice_similarity(u1, u2)
    0.38
    >>> consice_similarity(u1, u3)
    0.32
    """
    length = len(user1)
    above = 0
    for i in range(length):
        if user1[i] != 'N/A' and user2[i] != 'N/A':
            above += user1[i] * user2[i]

    m, n = 0, 0
    for i in range(length):
        if user1[i] != 'N/A':
            m += user1[i] ** 2
        if user2[i] != 'N/A':
            n += user2[i] ** 2
    below = math.sqrt(m) * math.sqrt(n)
    if above == 0 or below == 0:
        return 0
    else:
        return round(above / below, 2)


python_ta.check_all(config={
    'extra-imports': ['json', 'math', 'tkinter', 'tkinter.messagebox', 'data_preprocessing'],
    # the names (strs) of imported modules
    'allowed-io': ['open_steam_games', 'open_user_review'],
    # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['E1136']
})
