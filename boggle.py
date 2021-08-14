# Authors: maormiz, michael3162
# Students We talked the exercise with: NO ONE.
# Internet pages we used: https://www.tutorialspoint.com/python/tk_listbox.htm
# INTRO TO CS 2019-2020 EXERCISE 12
# Additional Files:
# board.py, helper.py, extra.py, boggle_board_randomizer.py, screen.py,
# boggle_dict.txt, AUTHORS, README
#######################################################
from board import Board
from screen import Screen
from time import time
from extra import *
from helper import *
from sys import exit


class Game:
    """
    Game class, creates a boggle game object using classes Screen and Board
    :var __board: the game board (object in type Board)
    :var __score: the current score the player has
    :var __last_hint_request_time: the last time (in UNIX time) when the
    player asked for a hint.
    :var __words_to_be_found: words list that can be founded on the board
    :var __words_found: the words the player have already founded
    :var __screen: the screen object (object in type Screen)
    :var __time_left: the time left for the game
    :var __began: boolean, that says if the game has began or not
    """
    # constants
    GAME_TIME = 180  # initial time in seconds
    ALLOW_HINTS = True
    TIME_FOR_LOOP = 15  # how many time the loop should be ran (milli-seconds)
    HINT_LENGTH = 5  # length of a found hint (should be 2 or bigger)
    HINT_SCORE_COST = 10  # how many points costs one hint
    HINT_BREAK_TIME = 20  # time (in seconds) between hints
    WORDS_FILE = "boggle_dict.txt"  # legal words file

    def __init__(self):
        """
        Game constructor
        creates all the fields needed for the Game object
        """
        # CREATES A NEW GAME
        self.__board = Board()
        self.__score = 0
        self.__last_hint_request_time = 0
        # gets the words that can be founded list
        self.__words_to_be_found = get_words(Game.WORDS_FILE)
        self.__words_found = set()
        # the screen which is attached to the game
        self.__screen = Screen(self.game_loop, self.__board)
        self.__time_left = Game.GAME_TIME
        self.__began = False

    def run_game(self):
        """
        this method runs all the game, by calling the screen
        :return: None
        """
        self.__screen.run_game()

    def end_game(self):
        """
        ends the game according to the procedure (showing a message, score,
        ask the player if he wants to play another game etc)
        :return: None
        """
        play_again = self.__screen.end_game(self.__score)
        self.__score = 0
        self.__time_left = Game.GAME_TIME
        self.__last_hint_request_time = 0
        # gets the words that can be founded list
        self.__words_found = set()
        self.__board.clear_path()

        if play_again:
            self.__began = False
            self.run_game()
        else:
            # wants to exit
            exit()

    def __check_game_end(self):
        """
        Checks if the game should end. If time ran out or player clicked exit
        button
        :return:
        """
        if self.__time_left <= 0:
            # time has ended, end the game (get out of the loop)
            self.end_game()
            return True
        if self.__screen.get_want_to_quit():
            # the player wants to quit
            self.__screen.get_parent().destroy()
            return True
        return False

    def __check_word_submit(self):
        """
        checks if the player wants to submit a word. informs the player if it
        is not a legal word, has been found, or submitted. clears the path
        afterwards.
        :return: None
        """
        if self.__screen.get_want_to_submit():
            for cord in self.__board.get_path():
                self.__screen.color_button(cord, Screen.DEFAULT_BUTTON_COLOR)
            # want to check the word
            self.__screen.set_submit(False)
            word = self.__board.get_word_by_path(self.__board.get_path())
            if len(word) == 0:
                self.__screen.show_message("You have to pick a word", "red", 3)
                return
            if word.upper() in self.__words_to_be_found:
                if word not in self.__words_found:
                    # found a word!
                    self.__screen.add_word_to_words_list(word)
                    # the path is a word
                    self.add_score(len(word))
                    self.__words_found.add(word)
                    self.__screen.show_message("You Found The Word " + word
                                               + "!", "green", 3)
                else:
                    self.__screen.show_message("You have already found "
                                               + word + "!", "red", 3)
            else:
                self.__screen.show_message("The word " + word + " does not " +
                                           "exist.", "red", 3)
            self.__board.clear_path()

    def update_clock(self):
        """
        self calling function, calls every 1 second to update the left time
        :return: None
        """
        if self.__began:
            self.__time_left -= 1
            self.__screen.get_parent().after(1000, self.update_clock)

    def game_loop(self):
        """
        runs the game, and calls this function again and again. main game loop.
        :return: None
        """
        if self.__screen.get_started():  # game has started
            self.__screen.set_started(False)
            self.__time_left += 1   # doesn't "steal" a second
            self.__began = True
            self.update_clock()
        if self.__check_game_end():
            return
        if self.__screen.get_want_a_hint():
            self.hint()
        self.__check_word_submit()
        self.__screen.update_screen(self.__time_left, self.__score)
        # repeat this function:
        self.__screen.get_parent().after(Game.TIME_FOR_LOOP, self.game_loop)

    def add_score(self, word_length):
        """
        updates score according to formula using the word's length
        :param word_length: word's length
        :return: None
        """
        self.__score = self.__score + (word_length ** 2)

    def hint(self):
        """
        checks if a hint was requested, and if it is possible to give it. if
        so, shows the hint. otherwise, shows the player an informative message
        :return: None
        """
        if not self.__began:
            # game has not even started
            return
        if not self.ALLOW_HINTS:
            self.__screen.show_message("Sorry but no hints available.",
                                       "gray", 5)
        if self.__score >= Game.HINT_SCORE_COST:  # the player has enough score
            if self.__last_hint_request_time + Game.HINT_BREAK_TIME <= time():
                # enough time passed since the player's last request
                hint = get_hint(self.__board, Game.HINT_LENGTH,
                                self.__words_to_be_found, self.__words_found)
                if not hint:
                    # no hint available
                    self.__screen.show_message("Sorry but no hints available.",
                                               "gray", 5)
                else:
                    hint_path = []
                    # color the start of the hint (not all of it!)
                    for cords in self.__board.get_cords():
                        self.__screen.color_button(cords,
                                                   Screen.DEFAULT_BUTTON_COLOR)

                    for hint_cord_index in range(Game.HINT_LENGTH // 2):
                        hint_path.append(hint[hint_cord_index])
                        self.__screen.color_button(hint[hint_cord_index],
                                                   Screen.HINT_BUTTON_COLOR)
                    hint_starts_with = self.__board.get_word_by_path(hint_path)
                    self.__screen.show_message("Your hint starts with: " +
                                               hint_starts_with, "green", 8)
                    # set the last request time to now
                    self.__last_hint_request_time = time()
                    self.__score -= Game.HINT_SCORE_COST
            else:
                time_left_for_hint = self.__last_hint_request_time \
                                     + Game.HINT_BREAK_TIME - time()
                self.__screen.show_message("You have to wait " +
                                           str(round(time_left_for_hint)) +
                                           " seconds for your next hint!",
                                           "red", 5)
        else:
            self.__screen.show_message("You don't have enough score for a "
                                       "hint!", "red", 5)


if __name__ == "__main__":
    # create a new game and play
    new_game = Game()
    new_game.run_game()
