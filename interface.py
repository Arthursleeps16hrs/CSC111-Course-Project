"""CSC111 Winter 2021 Final Project Part 3: Interface

Instructions
===============================

This Python module constructs an interface for users to do recommendation on games and game friends.
With selecting the option between user id and favorite game's name, and typing user id/ game's name,
users will obtain a new pop-up windows with an unique recommendation.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Yanke Mao, Yiteng Sun, Weiheng Wang and Jiaxu Li.
"""


####################################################################################################
# Part 3: Construct an interface for users to do recommendation
####################################################################################################

from typing import Union
import tkinter as tk
import tkinter.messagebox
import python_ta
import computation


def recommend(method: str, input_id: str, graph: computation.GameRecommendationGraph) \
        -> Union[list[tuple[str, str]], str]:
    """Using the certain method to recommend games with the input id/app name.
    Return a list of recommended games/game users together with their url.

    Precondition:
        - method1 in {'user id', 'favorite game id'}
    """
    if method == 'user id':
        return recommend_user_id(input_id, graph)
    elif method == 'favorite game id':
        return recommend_game_id(input_id, graph)
    else:
        raise ValueError


def print_result(method: str, input_id: str, graph: computation.GameRecommendationGraph) -> None:
    """
    Using the certain method to recommend games/game friends with the input id/app name.
    Show a messagebox including recommended games together with their url.
    Precondition:
        - method2 in {'user id', 'favorite game id'}
    """
    recommended_games = recommend(method, input_id, graph)
    if recommended_games == 'out of range':
        error_message = 'Sorry, the input id is not in our library. ' \
                        'We are very sorry we can"t make recommendation for this id.' \
                        '(Please be sure entering letter capitalization correctly. ' \
                        'The identification of game names is strict.'
        tkinter.messagebox.showwarning(title='Recommendation Games/Friends',
                                       message=error_message)
    elif recommended_games == 'No recommended games':
        error_message = 'We are very sorry that there is no recommended similar game ' \
                        'to your favorite game.'
        tkinter.messagebox.showinfo(title='Recommendation Games/Friends',
                                    message=error_message)
    elif recommended_games == 'No recommended friends':
        error_message = 'We are very sorry that there is no recommended similar users to you ' \
                        'in our library.'
        tkinter.messagebox.showinfo(title='Recommendation Games/Friends',
                                    message=error_message)
    else:
        message_so_far = ''
        for game in recommended_games:
            message_so_far += 'ID: ' + game[0] + ', URL: ' + game[1] + '\n'
        tkinter.messagebox.showinfo(title='Recommendation Games/Friends', message=message_so_far)


def recommend_user_id(user_id: str, graph: computation.GameRecommendationGraph) \
        -> Union[list[tuple[str, str]], str]:
    """
    Recommend at most 10 game friends to users with a certain user_id.
    Return a list of recommended friends together with their url.
    """
    return graph.find_similar_player(user_id, 10)


def recommend_game_id(game_name: str, graph: computation.GameRecommendationGraph) \
        -> Union[list[tuple[str, str]], str]:
    """
    Recommend at most 10 games to users with their favorite game name.
    Return a list of recommended games together with their url.
    """
    return graph.recommend_games(game_name, 10)


def recommend_interface(graph: computation.GameRecommendationGraph) -> None:
    """
    Construct an interface for users to make games recommendations based on a
    certain game id or a certain user id. User can choose the method of recommendation freely
    (with a game id or a user id). And after entering the id number, users can press the
    'Recommend!' button to get their unique game recommendation list.
    """
    # initialize the interface window
    window = tk.Tk()
    window.title('Games and Friends Recommendation')
    window.geometry('500x300')
    tk.Label(window, text='Welcome', font=('Arial', 16)).pack()

    # Use Radiobutton for users to choose the way to do recommendation
    method = tk.StringVar()
    method.set('user id')
    r1 = tk.Radiobutton(window, text='user id (recommend game friends)',
                        variable=method, value='user id')
    r1.pack()
    r2 = tk.Radiobutton(window, text='favorite game name (recommend games)',
                        variable=method, value='favorite game id')
    r2.pack()

    # Construct the entry box for users to enter id number
    id_entry = tk.Entry(window, show=None, font=('Arial', 14))
    id_entry.pack()

    # Construct the start button 'Recommend!' for users to start recommendation
    db = tk.Button(window, text="Recommend!",
                   command=(lambda: print_result(method.get(), id_entry.get(), graph)))
    db.pack()

    window.mainloop()


python_ta.check_all(config={
    'extra-imports': ['json', 'math', 'tkinter', 'tkinter.messagebox', 'computation'],
    # the names (strs) of imported modules
    'allowed-io': ['open_steam_games', 'open_user_review'],
    # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['E1136']
})
