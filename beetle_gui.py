#!/usr/bin/env python3
"""CS 424 Program 1

@author Jacob Rigby

The dice game Beetle, developed using Python 3.6.1, using a Tcl/Tk GUI"""

from random import randint
import signal
import sys  # For capturing Ctrl+C
import os
from tkinter import *
from tkinter.ttk import *

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
        percent_complete = sum([self._body, self._head,
                                self._left_legs, self._right_legs,
                                self._left_antenna, self._right_antenna,
                                self._left_eye, self._right_eye]) * 100 / 8
        return '{} is {}% complete'.format(self.name, percent_complete)

    def print(self):
        """Prints string representation directly to console"""
        print(self)

    def complete(self) -> bool:
        """Returns true if beetle is complete and the game has been won"""
        return self._body and self._head and \
               self._left_legs and self._right_legs and \
               self._left_antenna and self._right_antenna and \
               self._left_eye and self._right_eye


class TkBeetle(Beetle):
    """A Beetle that can also draw itself to a Tk label"""
    def __init__(self, name=None, imageLabel=None):
        super().__init__(self, name)
        self._image_label = imageLabel

    def draw(self):
        """Draws the beetle to imagelabel using included gif images"""
        image = PhotoImage(file='right_eye.gif') #TODO choose the right file based on whats complete
        self._image_label['image'] = image


class Game:
    """Class representing a single game.

    One instance will be created for each new game."""
    def __init__(self, num_players=2):
        """Sets up a new game"""
        self.__players = []
        for i in range(num_players):
            playername = "Player " + str(i+1)
            self.__players.append(Beetle(playername))
        self.__die = Die()

    def turn(self):
        """Takes a turn for the current player."""
        for player in self.__players:
            roll = self.__die.roll()
            player.turn(roll)
            print(player.name, 'rolled a', roll)
            if player.complete():
                if __name__ == '__main__':
                    if player.name is not None:
                        print(player.name, "wins!")
                    print("GAME OVER")
                yield True  # yield returns a generator objectthat keeps track of its internal state
            yield False     # so we can call turn multiple times per round, once for each player

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
        """Initialize the window"""
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        image = PhotoImage(file='right_eye.gif') #TODO change to none.gif
        self._beetle_1 = Label(self)
        self._beetle_1['image'] = image
        self._beetle_1.grid(column=0, row=0, sticky=(N, W))
        self._beetle_2 = Label(self)
        self._beetle_2['image'] = image
        self._beetle_2.grid(column=1, row=0, sticky=(N, E))

        self._testtext = Label(self, text="Testing")
        self._testtext.grid(column=0, row=1, sticky=(N, W, S, E))


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
                exit()
            # os.system('cls' if os.name == 'nt' else 'clear')

        except KeyboardInterrupt:
            print()
            exit()


def exit():
    """Prints goodbye and quits the program"""
    print("Goodbye.")
    sys.exit(0)

def main():
    """Sets up and runs the Tcl/Tk GUI"""
    root = Tk()
    root.title("Beetle by Jacob Rigby")

    app = Application(parent=root)

    app.mainloop()

if __name__ == '__main__':
    main()
