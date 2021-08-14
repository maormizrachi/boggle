# Authors: maormiz, michael3162
# Students We talked the exercise with: NO ONE.
# Internet pages we used: https://stackoverflow.com/questions/51369844/
# https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# INTRO TO CS 2019-2020 EXERCISE 12
# Additional Files:
# boggle.py, extra.py, board.py, boggle_board_randomizer.py, helper.py,
# boggle_dict.txt, AUTHORS, README
#######################################################
import tkinter
from tkinter import messagebox
from time import time
from helper import get_time_show


class Screen:
    """
    Screen class. Creates a screen object, takes care of all GUI performances.
    :var __parent: the tkinter graphic root
    :var __game_loop_func: the function which is the main game loop, should
    be in the game object
    :var __board: the board object
    """
    WINDOW_NAME = "Boggle"
    SCREEN_WIDTH = 550
    SCREEN_HEIGHT = 500
    SPACE = 12  # how much space does the board have
    WORDS_LIST_HEIGHT = 6  # number of words the words listbox shows
    GAME_BUTTONS_SIZE = 2
    SECONDS_TO_BE_RED = 10
    TIME_LABEL_NAME = "time"
    SCORE_LABEL_NAME = "score"
    QUIT_BUTTON_NAME = "quit"
    DEFAULT_LABEL_FONT_STYLE = ("Arial", 15)
    DEFAULT_MSG_FONT_STYLE = ("Arial", 12)
    DEFAULT_BUTTON_FONT_STYLE = ("Arial", 13)
    GAME_BUTTONS_FONT_STYLE = ("Arial", 15)
    PATH_BUTTON_COLOR = "#66ffb3"
    HINT_BUTTON_COLOR = "orange"
    DEFAULT_BUTTON_COLOR = "#ccf2ff"  # buttons' color
    BUTTONS_FRAME_COLOR = "#e5f2ff"  # buttons background color
    BACKGROUND = "#e6f9ff"
    HINT_KEY = "h"
    EXIT_KEY = "q"
    SUBMIT_KEY = "\\r"

    def __init__(self, game_loop_function, board):
        """
        Screen constructor. Creates a screen object with wanted fields.
        :param game_loop_function: main game loop
        :param board: board
        """
        self.__parent = tkinter.Tk()  # creates tkinter window
        self.__parent.title(Screen.WINDOW_NAME)
        self.__game_loop_func = game_loop_function
        self.__pre_start()
        self.__board = board  # object of the board
        self.__create_screen_objects()  # creates all screen objects

    def __pre_start(self):
        """
        resets all the screen's attributes, in order to start a new game
        :return: None
        """
        self.__last_widget_hover = None
        self.__want_to_quit = False
        self.__want_to_submit = False
        self.__game_started = False
        self.__message_end_time = 0
        self.__buttons = dict()  # dict of buttons: tuple of cords -> object
        self.__labels = dict()  # dict of labels: name of label -> object
        self.__word_list = None
        self.__current_word = None
        self.__start_button = None  # object of start button
        self.__keyboard_keys_list = list()  # will be checked every iteration

    def run_game(self):
        """
        runs the GUI, by calling the main loop
        :return: None
        """
        self.__game_loop_func()
        self.__parent.mainloop()

    def __create_drag_event(self, cords):
        """
        creates drag mouse option on all board buttons.
        :param cords: coordinates of button
        :return: button drag function
        """

        def button_drag(event):
            self.__board.add_to_path(cords)
            # what widget we are hovering on
            widget = event.widget.winfo_containing(event.x_root, event.y_root)
            if self.__last_widget_hover != widget:
                # hovering on a new button!
                current_widget = widget
                # set hover event as this event:
                current_widget.event_generate("<<B1-Enter>>")

        return button_drag

    def __button_release(self, event):
        """
        what happens when a button is being released
        :param event: event data (tkinter parameter)
        :return: None
        """
        self.__last_widget_hover = None
        # send the path
        self.set_submit(True)

    def __button_hover_event(self, cords):
        """
        creates a special function which tells the tkinter window what to do
        when a button is being hovered (in order to select the word)
        :param cords: event data (tkinter parameter)
        :return: None
        """

        def on_hover(event):
            self.__board.add_to_path(cords)

        return on_hover

    def get_parent(self):
        """
        :return: returns the parent (root), the tkinter's screen main object
        """
        return self.__parent

    def get_want_to_quit(self):
        """
        this method will be checked by Game, and returns True if the player
        wants to quit
        :return: True if the player wants to quit, otherwise False
        """
        return self.__want_to_quit or \
            "'" + Screen.EXIT_KEY + "'" in self.__keyboard_keys_list

    def get_want_to_submit(self):
        """
        get if player wants to submit a word
        :return: True or False
        """
        # via button, or via keyboard
        return self.__want_to_submit \
            or "'" + Screen.SUBMIT_KEY + "'" in self.__keyboard_keys_list

    def get_started(self):
        """
        :return: True or False if start button clicked
        """
        return self.__game_started

    def get_want_a_hint(self):
        """
        checks if a hint was requested
        :return: True or False
        """
        return "'" + Screen.HINT_KEY + "'" in self.__keyboard_keys_list

    def set_started(self, boolean):
        """
        set started field
        :param boolean: boolean expression
        :return: None
        """
        self.__game_started = boolean

    def set_submit(self, value):
        """
        set submit
        :param value: boolean expression
        :return: None
        """
        self.__want_to_submit = value

    def set_want_to_quit(self):
        """
        set want to quit field into True
        :return: None
        """
        self.__want_to_quit = True

    def add_word_to_words_list(self, word):
        """
        gets a word and adds it to the words list on the screen
        :param word: a word to be added
        :return: None
        """
        if self.__word_list is not None:
            self.__word_list.insert(self.__word_list.size() + 1, word)

    def __create_end_platform(self, score, words_found):
        """
        creates an end platform, which shows the player his score and
        the words he founded
        :param score: score the player achieved
        :param words_found: the words the player found
        :return: None
        """
        # create a temporary big frame
        big_frame = tkinter.Frame(self.__parent, bg=Screen.BACKGROUND,
                                  width=400, height=400)
        big_frame.pack()
        # message and score
        main_message = tkinter.Label(big_frame,
                                     bg=Screen.BACKGROUND,
                                     font=Screen.DEFAULT_LABEL_FONT_STYLE,
                                     text="Game has ended!")
        score_conclusion = tkinter.Label(big_frame,
                                         bg=Screen.BACKGROUND,
                                         font=Screen.DEFAULT_LABEL_FONT_STYLE,
                                         fg="blue", text="You got " +
                                                         str(score) +
                                                         " points!")
        main_message.grid()
        score_conclusion.grid(row=1, column=0)
        # words list, and the design of the list:
        words_you_found = tkinter.Label(big_frame,
                                        bg=Screen.BACKGROUND,
                                        text="The words you found: ",
                                        font=Screen.DEFAULT_LABEL_FONT_STYLE)
        wrds_lst = ""
        row_length = 0
        for word_index in range(len(words_found)):
            if row_length >= 35:
                row_length = 0
                wrds_lst += "\n"
            if word_index == len(words_found) - 1:
                wrds_lst += words_found[word_index]
            else:
                wrds_lst += words_found[word_index] + ", "
            row_length += len(words_found[word_index]) + 2
        # add the words to the screen
        the_words = tkinter.Label(big_frame, bg=Screen.BACKGROUND,
                                  text=wrds_lst, font=("Arial", 12))
        words_you_found.grid(row=2, column=0)
        the_words.grid(row=3, column=0)

    def end_game(self, score):
        """
        ends the game, and asks the player if he wants to play another game
        :param score: the amount of score the player achieved
        :return: True if
        """
        words_found = self.__word_list.get(0, self.__word_list.size())
        for frame in self.__parent.winfo_children():
            # clear board from all what it has
            frame.destroy()
        self.__create_end_platform(score, words_found)
        # ask for another game
        answer = tkinter.messagebox.askquestion('Game is over',
                                                'Time is out! ' +
                                                'Would you like to play '
                                                'another game?')
        if answer == 'no':
            self.__parent.destroy()
            return False
        else:
            self.__pre_start()  # reset screen data
            self.__board.randomize()
            for frame in self.__parent.winfo_children():
                # clear board from all what it has
                frame.destroy()
            self.__create_screen_objects()
            return True

    def __keyboard_key_event(self, event):
        """
        when the player clicks a keyboard key, it adds it to the clicked keys
        :param event: the event (click) data from tkinter
        :return: None
        """
        self.__keyboard_keys_list.append(repr(event.char))

    def __create_bottom_frame(self):
        """
        creates the bottom frame of the game with words list, current word,
        scroll bar, and a message
        :return: None
        """
        # create the frame itself
        bottom_frame = tkinter.Frame(self.__parent, bg=Screen.BACKGROUND,
                                     width=120, height=40)
        bottom_frame.grid(row=2, column=1)
        # semi-frame of the words only

        words_frame = tkinter.Frame(bottom_frame, bg=Screen.BACKGROUND,
                                    width=100, height=40)
        # current word section
        current_word = tkinter.Label(bottom_frame,
                                     bg=Screen.BACKGROUND, height=2,
                                     font=Screen.DEFAULT_LABEL_FONT_STYLE)
        self.__current_word = current_word
        current_word.grid(row=0, column=0)

        # word list + scrollbar
        word_list = tkinter.Listbox(words_frame,
                                    bg=Screen.BACKGROUND,
                                    width=30, height=Screen.WORDS_LIST_HEIGHT)
        self.__word_list = word_list
        word_list.grid(row=0, column=0)
        scrollbar = tkinter.Scrollbar(words_frame, orient="vertical",
                                      bg=Screen.BACKGROUND,
                                      command=word_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        word_list.config(yscrollcommand=scrollbar.set)
        words_frame.grid(row=1, column=0)

        # message
        message = tkinter.Label(bottom_frame, width=40,
                                bg=Screen.BACKGROUND,
                                font=Screen.DEFAULT_MSG_FONT_STYLE)
        self.__message_label = message
        message.grid(row=2, column=0)

    def __create_side_frame(self):
        """
        creates the side frame with quit button, hint button, time and score
        labels
        :return: None
        """

        def ask_for_hint_func():
            self.__keyboard_keys_list.append("'" + Screen.HINT_KEY + "'")

        # create side frame (mostly settings):
        side_frame = tkinter.Frame(self.__parent, bg=Screen.BACKGROUND,
                                   width=50, height=100)
        side_frame.grid(row=1, column=2)

        # create labels (time and score)
        time_left_label = tkinter.Label(side_frame,
                                        bg=Screen.BACKGROUND,
                                        font=Screen.DEFAULT_LABEL_FONT_STYLE)
        score_label = tkinter.Label(side_frame,
                                    bg=Screen.BACKGROUND,
                                    font=Screen.DEFAULT_LABEL_FONT_STYLE)
        self.__labels[Screen.TIME_LABEL_NAME] = time_left_label
        self.__labels[Screen.SCORE_LABEL_NAME] = score_label

        # create quit button:
        quit_button = tkinter.Button(side_frame,
                                     bg="#ffb3b3",
                                     font=Screen.DEFAULT_BUTTON_FONT_STYLE,
                                     text="End Game",
                                     command=self.set_want_to_quit)
        quit_button.grid(row=0, column=0)

        hint_button = tkinter.Button(side_frame,
                                     font=Screen.DEFAULT_BUTTON_FONT_STYLE,
                                     bg=Screen.HINT_BUTTON_COLOR,
                                     text="Hint",
                                     command=ask_for_hint_func)
        hint_button.grid(row=len(self.__labels) + 1, column=0)

    def __create_buttons(self):
        """
        creates all board buttons and adds them to the tkinter window
        :return:
        """
        buttons_frame = tkinter.Frame(self.__parent, width=20, height=20,
                                      bg=Screen.BUTTONS_FRAME_COLOR)
        buttons_frame.grid(row=1, column=1)

        for cord in self.__board.get_cords():
            # create a button for each coordinate
            button_obj = tkinter.Button(buttons_frame,
                                        font=Screen.GAME_BUTTONS_FONT_STYLE,
                                        width=Screen.GAME_BUTTONS_SIZE,
                                        bg=Screen.DEFAULT_BUTTON_COLOR,
                                        text=self.__board.get_cords_letter(
                                            cord))
            # add actions and events
            button_obj.bind("<B1-Motion>", self.__create_drag_event(cord))
            button_obj.bind("<<B1-Enter>>", self.__button_hover_event(cord))
            button_obj.bind("<ButtonRelease-1>", self.__button_release)
            self.__buttons[cord] = button_obj

        for row in sorted([cord[0] for cord in self.__buttons.keys()]):
            # space between rows
            space_frame = tkinter.Frame(buttons_frame, height=Screen.SPACE,
                                        bg=Screen.BUTTONS_FRAME_COLOR)
            space_frame.grid(row=2 * row + 2)
            for col in sorted([cord[1] for cord in self.__buttons.keys()
                               if cord[0] == row]):
                # show button in cords (row, col)
                self.__buttons[(row, col)].grid(row=2 * row + 1,
                                                column=2 * col + 1)
                # show space
                space_frame = tkinter.Frame(buttons_frame,
                                            bg=Screen.BUTTONS_FRAME_COLOR,
                                            width=Screen.SPACE)
                space_frame.grid(row=2 * row + 1, column=2 * col + 2)

    def __press_start_button(self):
        """
        once start button is pressed, destroys it, creates the board and
        changes the game stated field into True
        :return: None
        """
        # keyboard events will be treated like that
        self.__parent.bind("<Key>", self.__keyboard_key_event)
        self.__start_button.destroy()  # remove start button
        self.__game_started = True
        self.__create_buttons()  # creates all the buttons

    def __create_screen_objects(self):
        """
        creates all screen objects
        :return: None
        """
        self.__parent["bg"] = Screen.BACKGROUND
        frame = tkinter.Frame(self.__parent)
        logo_label = tkinter.Label(frame, text="Boggle",
                                   bg=Screen.BACKGROUND,
                                   fg="#809fff", font=("Arial", 40))
        logo_label.pack()
        frame.grid(row=0, column=1)

        # invisible frame (to make a space between the corner and the game)
        invisible_frame = tkinter.Frame(self.__parent,
                                        bg=Screen.BACKGROUND,
                                        width=15, height=15)
        invisible_frame.grid(row=1, column=0)

        self.__parent.geometry(str(Screen.SCREEN_WIDTH) + "x" +
                               str(Screen.SCREEN_HEIGHT))

        temp_frame = tkinter.Frame(self.__parent,
                                   bg=Screen.BUTTONS_FRAME_COLOR,
                                   width=10, height=5)
        start_button = tkinter.Button(temp_frame, width=10, height=5,
                                      bg="#ccf2ff", text="Start",
                                      font=("Arial", 25),
                                      command=self.__press_start_button)
        temp_frame.grid(row=1, column=1)

        start_button.grid(row=0, column=2)
        self.__start_button = start_button
        self.__create_bottom_frame()
        self.__create_side_frame()
        # show on the screen each label and each button
        label_counter = 1  # should be started on row *1*
        for label in self.__labels:
            self.__labels[label].grid(row=label_counter, column=0)
            label_counter += 1

    def show_message(self, message, message_color, time_to_show):
        """
        shows a label on the screen, which can be a message for the player
        :param message: a message to the player
        :param message_color: the message's color
        :param time_to_show: the time the message will be shown
        :return: None
        """
        self.__message_label["text"] = str(message)
        self.__message_label["fg"] = str(message_color)
        self.__message_end_time = time() + time_to_show

    def color_button(self, coordinate, color):
        """
        changes the button in the given coordinates to the given color
        :param coordinate: given coordinates of the button
        :param color: given color to change to
        :return: None
        :exception: raises ValueError if the coordinate does not exists
        """
        if coordinate in self.__buttons:
            self.__buttons[coordinate]["bg"] = color
        else:
            # not exists
            raise ValueError("Coordinate is not on board.")

    def update_screen(self, time_left, score):
        """
        shows the buttons (which are together the graphic version of board)
        on the screen, also shows the time left and score
        :return: None
        """
        # clear keyboard events:
        self.__keyboard_keys_list.clear()
        # labels:
        if time_left <= Screen.SECONDS_TO_BE_RED:
            # last seconds of the game
            self.__labels[Screen.TIME_LABEL_NAME]["fg"] = "red"
        time_left = "Time Left: " + get_time_show(time_left)
        self.__labels[Screen.TIME_LABEL_NAME].configure(text=time_left)
        score = "Score: " + str(score)
        self.__labels[Screen.SCORE_LABEL_NAME].configure(text=score)

        # current word:
        current_word = self.__board.get_word_by_path(self.__board.get_path())
        if current_word != "":
            self.__current_word["text"] = "Word: " + current_word
        else:
            self.__current_word["text"] = ""  # reset text

        # buttons (change their colors if needed)
        for button_cord in self.__buttons:
            # update each button (if is clicked or not)
            if button_cord in self.__board.get_path():
                self.color_button(button_cord, Screen.PATH_BUTTON_COLOR)
        # message
        if self.__message_end_time < time():
            self.__message_label["text"] = ""
