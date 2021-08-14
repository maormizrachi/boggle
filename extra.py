# Authors: maormiz, michael3162
# Students We talked the exercise with: NO ONE.
# INTRO TO CS 2019-2020 EXERCISE 12
# Additional Files:
# boggle.py, board.py, helper.py, boggle_board_randomizer.py, screen.py,
# boggle_dict.txt, AUTHORS, README
# EXTRA FILE WHICH CONTAINS EXTRA FUNCTIONS
#######################################################
from random import choice


def _get_hint_helper(path, board, length):
    """
    this recursive function returns all the possible ways of paths with a
    given length, starting a path.
    :param path: a current path
    :param board: the board (to know the coordinates)
    :param length: the length of the wanted path
    :return: list of lists of paths
    """
    if length == 1:
        return [path]
    possible_ways = list()
    for direction in board.ALLOWED_DIRECTIONS:
        # return all the possible paths which continue the given path, with
        # a length of length, by using a recursion
        next_cell = (path[-1][0] + direction[0], path[-1][1] + direction[1])
        if next_cell in board.get_cords() and next_cell not in path:
            # the cell is in the board (legal to reach) AND not visited yet
            for possible_continue in _get_hint_helper(path + [next_cell],
                                                      board, length - 1):
                possible_ways.append(possible_continue)
    return possible_ways


def get_hint(board, length, possible_words, founded):
    """
    by giving this function a board and a length of a wanted hint, it returns
    a possible way to find a word in the length *length*, starting with
    a random coordinate.
    :param board: the board to work with (object)
    :param length: the length of the wanted hint
    :param possible_words: list of all the possible words
    :param founded: list of all the founded words
    :return: a random possible way to select a word on the screen (a word
    in the given length)
    """
    tried_to_find_a_hint = list()  # coordinates we tried to find a hint there
    board_cords = sorted(board.get_cords())
    while True:
        if sorted(tried_to_find_a_hint) == board_cords:
            # tried all the coordinates, no hints
            break
        # until a hint will be found
        random_cords = choice(board.get_cords())  # get a random cords
        if random_cords in tried_to_find_a_hint:
            # we already tried, and couldn't find, so skip
            continue
        tried_to_find_a_hint.append(random_cords)
        hints = _get_hint_helper([random_cords], board, length)
        # from all the hints suggested, find only those who represent a word
        real_hints = [hint_path for hint_path in hints
                      if board.get_word_by_path(hint_path) in possible_words
                      and board.get_word_by_path(hint_path) not in founded]
        if real_hints:
            # not empty, return a random hint from what we have
            return choice(real_hints)
        # else, continue and find another hint
    # if we reached here, no hints available
    return []
