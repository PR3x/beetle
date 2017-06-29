#!/usr/bin/env python3
"""CS 424 Program 1

@author Jacob Rigby

The dice game Beetle, developed using Python 3.6.1"""

from random import randint
import signal
import sys  # For capturing Ctrl+C

class Die(object):
    """Die that can roll between 1 and given number. Default of 6"""

    def __init__(self, num_sides=6):
        """Default number of sides is 6"""
        self.__num_sides = num_sides


    def roll(self) -> int:
        """Generates a random number"""
        return randint(1, self.__num_sides)


class Beetle(object):
    """The core class of this program.

    Holds data related to game state for a single player."""

    def __init__(self):
        """Creates a new gameboard for a player"""
        self.__body = False
        self.__head = False
        self.__left_legs = False
        self.__right_legs = False
        self.__left_antenna = False
        self.__right_antenna = False
        self.__left_eye = False
        self.__right_eye = False


    def turn(self, roll) -> bool:
        """Represents the act of taking a turn in the game.

        Moves forward a step in the state machine"""

        # Create the body if 1 is rolled
        if not self.__body and roll == 1:
            self.__body = True
            return True

        # Create the head if 2 is rolled
        if not self.__head and roll == 2:
            self.__head = True
            return True

        # Create the left legs if 3 is rolled
        if not self.__left_legs and roll == 3:
            self.__left_legs = True
            return True

        # Create the right legs if 3 is rolled
        if not self.__right_legs and roll == 3:
            self.__right_legs = True
            return True

        # Create the left antenna if 4 is rolled
        if not self.__left_antenna and roll == 4:
            self.__left_antenna = True
            return True

        # Create the right antenna if 4 is rolled
        if not self.__right_antenna and roll == 4:
            self.__right_antenna = True
            return True

        # Create the left eye if 5 is rolled
        if not self.__left_eye and roll == 5:
            self.__left_eye = True
            return True

        # Create the right eye if 5 is rolled
        if not self.__right_eye and roll == 5:
            self.__right_eye = True
            return True

        return False  # we didn't move forward in the state machine



    def print(self) -> str:
        """Pretty string representation of the beetle"""
        return ""  #TODO Print ascii art!

    __str__ = print

    def complete(self) -> bool:
        """Returns true if beetle is complete and the game has been won"""
        return self.__body and self.__head and self.__left_legs and self.__right_legs and \
               self.__left_antenna and self.__right_antenna and self.__left_eye and self.__right_eye


class Game(object):
    """Class representing a single game.

    One instance will be created for each new game."""
    def __init__(self, num_players=2):
        """Sets up a new game"""
        self._players = []
        for _ in range(num_players):
            self._players.append(Beetle())
        self._die = Die()

    def turn(self):
        """Takes a turn for all players"""
        for player in self._players:
            player.turn(self._die.roll())
            if player.complete:
                print("GAME OVER")
                return True


def main():
    """Core loop of program. Runs the game until Ctrl+C to exit."""
    # Ensure KeyboardInterrupt is fired on SIGINT
    signal.signal(signal.SIGINT, signal.default_int_handler)

    while True:
        try:
            game = Game()

            while not game.turn():
                pass

            input("Press Enter to continue or Ctrl+C to exit.")

        except KeyboardInterrupt:
            print("\nGoodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
