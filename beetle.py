#!/usr/bin/env python3
"""CS 424 Program 1

@author Jacob Rigby

The dice game Beetle, developed using Python 3.6.1"""

from random import randint
import signal
import sys  # For capturing Ctrl+C
import os

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

    def __str__(self) -> str:
        """Pretty string representation of the beetle"""
        percent_complete = sum([self.__body, self.__head,
                                self.__left_legs, self.__right_legs,
                                self.__left_antenna, self.__right_antenna,
                                self.__left_eye, self.__right_eye]) * 12.5
        return '{} is {}% complete'.format(self.name, percent_complete)  #TODO Print ascii art!

    def print(self):
        """Prints string representation directly to console"""
        print(str(self))

    def complete(self) -> bool:
        """Returns true if beetle is complete and the game has been won"""
        return self.__body and self.__head and \
               self.__left_legs and self.__right_legs and \
               self.__left_antenna and self.__right_antenna and \
               self.__left_eye and self.__right_eye


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
        """Takes a turn for all players"""
        for player in self.__players:
            player.turn(self.__die.roll())
            print(player)
            if player.complete():
                if __name__ == '__main__':
                    if player.name is not None:
                        print(player.name, "wins!")
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
            # os.system('cls' if os.name == 'nt' else 'clear')

        except KeyboardInterrupt:
            print("\nGoodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
