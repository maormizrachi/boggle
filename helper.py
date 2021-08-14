# Authors: maormiz, michael3162
# Students We talked the exercise with: NO ONE.
# INTRO TO CS 2019-2020 EXERCISE 12
# Additional Files:
# boggle.py, extra.py, board.py, boggle_board_randomizer.py, screen.py,
# boggle_dict.txt, AUTHORS, README
#######################################################


def get_words(filename="boggle_dict.txt"):
    """
    this function gets a filename, and returns the list of the words that are
    in the file.
    :param filename: a file, defaulted with "boggle_dict.txt"
    :return: list of the words which are in the file
    """
    with open(filename, "r") as opened_file:
        # return the list of the words, after opening the file
        return set([word.replace("\n", "") for word in
                    opened_file.readlines()])


def get_time_show(game_time):
    """
    this function gets time in seconds and returns a string which represent
    the time in minutes and seconds (min: sec), to be shown on screen.
    :param game_time: the time in seconds
    :return: a string on the way the time will be shown on screen (min:sec)
    """
    minutes = game_time // 60
    if minutes <= 9:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    seconds = game_time % 60
    if seconds <= 9:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
    return minutes + ":" + seconds
