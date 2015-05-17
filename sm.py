# ------------------------------------------
# Name:     sm.py
# Purpose:  SteamMover will list all of the directories (games) under the steam Common dir. The user can select
#           a game and it will be moved to the specified directory. A symbolic link will be created to the
#           original directory so that Steam will still launch the game.
#
# Author:   Robin Siebler
# Created:  7/31/13
# ------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/31/13'

import sys
from games import Games

usage = """
SteamMover will present a list of games found in the specified location.
The game(s) you select will be moved to the location  you specified, providing there is room.

usage:  sm.py <path to Steam> <path to move games to>
   Ex:  sm.py "c:\program files\steam\steamapps\common" "g:\Steam Games\SteamApps\common"

"""


def display_menu(game_list):
    """Displays a menu with the game list.

    :param game_list: a list containing the Steam games
    """

    print('\nDiscovered Steam Games:\n')
    for index, item in enumerate(game_list, start=1):
        print('\t{}. {}'.format(index, item))

    print('\n Enter "q" to quit or "r" to redraw the menu\n')


def get_choice(game_list):
    """Find out what the user wants to do.

    :param game_list: a list containing the Steam games
    :return: a string containing either 'q', 'r' or the name of a game
    """

    while True:
        choice = input('Enter the number for the game you wish to move: ').lower()
        if ('q' or 'r') not in choice and not choice.isdigit():
            print("That is not a valid choice")
            continue
        if 'q' in choice or 'r' in choice:
            return choice

        choice = int(choice)
        if choice not in range(1, len(game_list)):
            print("That is not a valid choice")
            continue
        elif ' *' in game_list[choice - 1]:
            print('That game has already been moved')
        else:
            return game_list[choice - 1]


def parse_cmdline():
    """Parse the command-line. Validate that the correct number of params was provided.


    :return: the 2 game directories
    """

    if len(sys.argv) != 3:
        print(usage)
        print('\nAn invalid number of parameters was provided!\n')
        sys.exit(1)

    return sys.argv[1], sys.argv[2]


def main():
    steam_dir, remote_dir = parse_cmdline()
    games = Games(steam_dir, remote_dir)  # parse the command line
    games.validate_paths()
    games.update_games()

    choice = ''
    while choice != 'q':
        display_menu(games.game_list)
        choice = get_choice(games.game_list)
        if choice == 'q':
            print('\nExiting...')
            sys.exit()
        elif choice == 'r':
            continue  # start at the top of the loop and display the menu again
        else:
            games.move_game(choice)
            games.update_games()

if __name__ == "__main__":
    main()
