#!/usr/bin/env python3
"""CS 424 Program 1

@author Jacob Rigby
@date 6 July 2017

The dice game Beetle, developed using Python 3.6.1, using a Tk GUI"""

#    Copyright 2017 Jacob Rigby
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from random import randint
import signal
import sys  # For capturing Ctrl+C
from tkinter import *       # Tkinter GUI components
from tkinter.ttk import *   # Modern Tkinter ToolKit components

class Die:
    """Die that can roll between 1 and given number. Default of 6 sides"""

    def __init__(self, num_sides=6):
        """Default number of sides is 6"""
        self.__num_sides = num_sides

    def roll(self) -> int:
        """Generates a random number"""
        return randint(1, self.__num_sides)


class Beetle:
    """The core class of this program.

    Holds data related to game state for a single player."""

    def __init__(self, name=None):
        """Creates a new gameboard for a player"""
        self.name = name
        self._body = False
        self._head = False
        self._left_legs = False
        self._right_legs = False
        self._left_antenna = False
        self._right_antenna = False
        self._left_eye = False
        self._right_eye = False

    def turn(self, roll) -> bool:
        """Represents the act of taking a turn in the game.

        Moves forward a step in the state machine"""

        # Create the body if 1 is rolled
        if not self._body and roll == 1:
            print(self.name, "rolled a 1, built body")
            self._body = True
            return True

        # Create the head if 2 is rolled once 1 has already been rolled
        if self._body and not self._head and roll == 2:
            print(self.name, "rolled a 2, built head")
            self._head = True
            return True

        # Create the left legs if 3 is rolled
        if self._head and not self._left_legs and roll == 3:
            print(self.name, "rolled a 3, built left legs")
            self._left_legs = True
            return True

        # Create the right legs if 3 is rolled
        if self._left_legs and not self._right_legs and roll == 3:
            print(self.name, "rolled a 3, built right legs")
            self._right_legs = True
            return True

        # Create the left antenna if 4 is rolled
        if self._right_legs and not self._left_antenna and roll == 4:
            print(self.name, "rolled a 4, built left antenna")
            self._left_antenna = True
            return True

        # Create the right antenna if 4 is rolled
        if self._left_antenna and not self._right_antenna and roll == 4:
            print(self.name, "rolled a 4, built right antenna")
            self._right_antenna = True
            return True

        # Create the left eye if 5 is rolled
        if self._right_antenna and not self._left_eye and roll == 5:
            print(self.name, "rolled a 5, built left eye")
            self._left_eye = True
            return True

        # Create the right eye if 5 is rolled
        if self._left_eye and not self._right_eye and roll == 5:
            print(self.name, "rolled a 5, built right eye")
            self._right_eye = True
            return True

        return False  # we didn't move forward in the state machine

    def __str__(self) -> str:
        """Pretty string representation of the beetle"""
        # There are 8 parts, and 100 percent
        percent_complete = sum([self._body, self._head,
                                self._left_legs, self._right_legs,
                                self._left_antenna, self._right_antenna,
                                self._left_eye, self._right_eye]) * 100 / 8
        return '{} is {}% complete'.format(self.name, percent_complete)

    def print(self):
        """Prints string representation directly to console"""
        print(self)

    def complete(self) -> bool:
        """Returns true if beetle is complete and the game has been won

        All parts must exist."""
        return self._body and self._head and \
               self._left_legs and self._right_legs and \
               self._left_antenna and self._right_antenna and \
               self._left_eye and self._right_eye


class TkBeetle(Beetle):
    """A Beetle that can also draw itself to a Tk label"""
    def __init__(self, name=None, imageLabel=None, app=None):
        Beetle.__init__(self, name=name)
        self._image_label = imageLabel
        self._app = app

    def draw(self):
        """Draws the beetle to image_label using included gif images"""
        image = self._app.none_image
        if self._body:
            image = self._app.body_image
        if self._head:
            image = self._app.head_image
        if self._left_legs:
            image = self._app.left_legs_image
        if self._right_legs:
            image = self._app.right_legs_image
        if self._left_antenna:
            image = self._app.left_antenna_image
        if self._right_antenna:
            image = self._app.right_antenna_image
        if self._left_eye:
            image = self._app.left_eye_image
        if self._right_eye:
            image = self._app.right_eye_image
        self._image_label['image'] = image

    def turn(self, roll):
        """Represents the act of taking a turn in the game.

        Moves forward a step in the state machine,
        then draws itself to the screen"""
        # take a normal turn and store the result to return later
        # before drawing to the screen
        out = Beetle.turn(self, roll)
        self.draw()
        return out


class Game:
    """Class representing a single game.

    One instance will be created for each new game."""
    def __init__(self, app=None):
        """Sets up a new game"""
        self.__players = []
        self._app = app
        self.__players.append(TkBeetle("Player 1", imageLabel=app.beetle_1, app=app))
        self.__players.append(TkBeetle("Player 2", imageLabel=app.beetle_2, app=app))
        self.__die = Die()

    def turn(self):
        """Takes a turn for the current player."""
        for player in self.__players:
            roll = self.__die.roll()
            player.turn(roll)
            round_info = player.name + ' rolled a ' + str(roll)
            print(round_info)
            self._app.infotext['text'] = round_info
            if player.complete():
                if player.name is not None or player.name is not "":
                    print(player.name, "wins!")
                print("GAME OVER")
                yield True # yield returns a generator object that keeps track of its internal state

            yield False    # so we can call turn multiple times per round, once for each player
    def round(self):
        """Takes a turn for all players"""
        for turn in self.turn():
            if turn:
                return True
        return False


class Application(Frame):
    """Application class wrapping the main GUI frame"""
    def __init__(self, parent):
        Frame.__init__(self, parent, padding="3 3 12 12")
        self.setup()

    def setup(self):
        """Initialize the window and create some constants"""
        # We need to keep a reference to each of the images to keep them from
        # being garbage collected.
        # Also, they should be "public" so that the beetles can get to them
        self.none_image = PhotoImage(file='none.gif')
        self.body_image = PhotoImage(file='body.gif')
        self.head_image = PhotoImage(file='head.gif')
        self.left_legs_image = PhotoImage(file='left_legs.gif')
        self.right_legs_image = PhotoImage(file='right_legs.gif')
        self.left_antenna_image = PhotoImage(file='left_antenna.gif')
        self.right_antenna_image = PhotoImage(file='right_antenna.gif')
        self.left_eye_image = PhotoImage(file='left_eye.gif')
        self.right_eye_image = PhotoImage(file='right_eye.gif')

        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # beetle_1 and beetle_2 need to be "public" for the same reason as the images
        self.beetle_1 = Label(self)
        self.beetle_1['image'] = self.none_image
        self.beetle_1.grid(column=0, row=0, sticky=(N, W))

        self.beetle_2 = Label(self)
        self.beetle_2['image'] = self.none_image
        self.beetle_2.grid(column=2, row=0, sticky=(N, E))

        self.infotext = Label(self, text="Testing")
        self.infotext.grid(column=1, row=1, sticky=(W, S, E))

        self._beetle_1_button = Button(self, text="Roll", command=self.turn)
        self._beetle_1_button.grid(column=0, row=1, sticky=(W, S))

        self._beetle_2_button = Button(self, text="Roll", command=self.turn)
        self._beetle_2_button.grid(column=2, row=1, sticky=(E, S))

        for child in self.winfo_children():
            # go through every child and set some params
            child.grid_configure(padx=5, pady=5)

        # Set up the game last so everything is initialized
        self._game = Game(app=self)

    def turn(self):
        """Takes a turn in the game"""
        self._game.round()


def cli_main():
    """Main loop of program in basic CLI mode.

    Runs the game until exit requested."""
    # Ensure KeyboardInterrupt is fired on SIGINT
    signal.signal(signal.SIGINT, signal.default_int_handler)

    while True:
        try:
            game = Game()

            while not game.round():
                pass

            key = input("Press Enter to play again or q to exit. ")
            if key == 'q' or key == 'Q':
                exit_game()
            # os.system('cls' if os.name == 'nt' else 'clear')

        except KeyboardInterrupt:
            print()  # we need the extra newline
            exit_game()


def exit_game():
    """Prints goodbye and quits the program"""
    print("Goodbye.")
    sys.exit(0)

def main():
    """Sets up and runs the Tk GUI"""
    root = Tk()
    root.title("Beetle by Jacob Rigby")

    app = Application(parent=root)

    app.mainloop()

if __name__ == '__main__':
    main()
