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
            print(self.name, "rolled a 1, built body")
            self.__body = True
            return True

        # Create the head if 2 is rolled once 1 has already been rolled
        if self.__body and not self.__head and roll == 2:
            print(self.name, "rolled a 2, built head")
            self.__head = True
            return True

        # Create the left legs if 3 is rolled
        if self.__head and not self.__left_legs and roll == 3:
            print(self.name, "rolled a 3, built left legs")
            self.__left_legs = True
            return True

        # Create the right legs if 3 is rolled
        if self.__left_legs and not self.__right_legs and roll == 3:
            print(self.name, "rolled a 3, built right legs")
            self.__right_legs = True
            return True

        # Create the left antenna if 4 is rolled
        if self.__right_legs and not self.__left_antenna and roll == 4:
            print(self.name, "rolled a 4, built left antenna")
            self.__left_antenna = True
            return True

        # Create the right antenna if 4 is rolled
        if self.__left_antenna and not self.__right_antenna and roll == 4:
            print(self.name, "rolled a 4, built right antenna")
            self.__right_antenna = True
            return True

        # Create the left eye if 5 is rolled
        if self.__right_antenna and not self.__left_eye and roll == 5:
            print(self.name, "rolled a 5, built left eye")
            self.__left_eye = True
            return True

        # Create the right eye if 5 is rolled
        if self.__left_eye and not self.__right_eye and roll == 5:
            print(self.name, "rolled a 5, built right eye")
            self.__right_eye = True
            return True

        return False  # we didn't move forward in the state machine

    def __str__(self) -> str:
        """Pretty string representation of the beetle"""
        percent_complete = sum([self.__body, self.__head,
                                self.__left_legs, self.__right_legs,
                                self.__left_antenna, self.__right_antenna,
                                self.__left_eye, self.__right_eye]) * 100 / 8
        return '{} is {}% complete'.format(self.name, percent_complete)

    def print(self):
        """Prints string representation directly to console"""
        print(self)

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
                game_exit()
            # os.system('cls' if os.name == 'nt' else 'clear')

        except KeyboardInterrupt:
            print()
            game_exit()


def game_exit():
    """Prints goodbye and quits the program"""
    print("Goodbye.")
    sys.exit(0)


if __name__ == "__main__":
    cli_main()
