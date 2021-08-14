# Authors: maormiz, michael3162
# Students We talked the exercise with: NO ONE.
# INTRO TO CS 2019-2020 EXERCISE 12
# Additional Files:
# boggle.py, extra.py, helper.py, boggle_board_randomizer.py, screen.py,
# boggle_dict.txt, AUTHORS, README
#######################################################
import boggle_board_randomizer


class Board:
    """
    Board class, creates a board object made of random letters
    :var __board: the board itself, a list of lists which conclude the letters
    :var __path: the current path the player did, on the screen
    """
    # set of all the allowed moving steps allowed (row, col)
    ALLOWED_DIRECTIONS = {(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1),
                          (1, -1), (-1, 1)}

    def __init__(self):
        """
        Board constructor. creates the board with wanted fields.
        """
        self.__board = list()
        self.randomize()  # makes a random board
        self.__path = []  # the current path the player did

    def randomize(self):
        """
        creates the random board according to given board randomize function
        :return: None
        """
        self.__board = boggle_board_randomizer.randomize_board()

    def get_cords(self):
        """
        :return: a list of all the cords which are in the board
        """
        cords_list = list()
        for row in range(len(self.__board)):
            # adds to the list all the cords in this row
            for col in range(len(self.__board[row])):
                cords_list.append((row, col))
        return cords_list  # returns all the cords

    def get_board(self):
        """
        board getter.
        :return: the board itself
        """
        return self.__board

    def get_cords_letter(self, cords):
        """
        gets the letter according to the board's coordinates
        :param cords: coordinates
        :return: letter on coordinates
        """
        return self.__board[cords[0]][cords[1]]

    def get_path(self):
        """
        gets the current path
        :return: path
        """
        return self.__path

    def get_word_by_path(self, path):
        """
        gets the word according to given path
        :param path: path
        :return: word
        """
        # add the letter in each coordinate to the word
        word_in_path = ""
        for cord in path:
            word_in_path += self.get_cords_letter(cord)
        return word_in_path  # returns the word

    def clear_path(self):
        """
        clears path
        :return: None
        """
        self.__path = []

    def add_to_path(self, cords):
        """
        adds coordinates to path if legal
        :param cords: coordinates
        :return: None
        """
        if cords not in self.__path:
            self.__path = self.__path + [cords]
            if not self.__is_possible_path():
                # keep the legal path till now
                self.__path = self.__path[:-1]

    def __is_possible_path(self):
        """
        checks the path that the player did (coordinate by coordinate), and
        returns True if the path is valid, according to the legal moving
        directions
        :return: True if the path is legal, otherwise False
        """
        for path_index in range(1, len(self.__path)):
            # for each coordinate in the path (recognized by index) check
            # the movement the player did, and if it it not valid return False
            current_place = self.__path[path_index]
            previous_place = self.__path[path_index - 1]
            move = (current_place[0] - previous_place[0],
                    current_place[1] - previous_place[1])
            if move not in Board.ALLOWED_DIRECTIONS:
                # the movement the player did is not valid!
                return False
        # if we reached here, all the moves were valid, so it is OK
        return True
