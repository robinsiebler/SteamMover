# ------------------------------------------
# Name:     games.py
# Purpose:  A class for Steam games
#
# Author:   Robin Siebler
# Created:  8/4/13
# ------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '8/4/13'

import os
import sys
import shutil
import tempfile
import util


class Games:
    """The class to deal with Steam games."""
    def __init__(self, steam_dir, remote_dir):
        self.steam_dir = steam_dir
        self.remote_dir = remote_dir
        self.local_games = []
        self.remote_games = []
        self.remote_installed_games = []

    def move_game(self, curr_path, dest_path, create_symlink=False):
        """Move a game from the current dir to the destination dir.
        If the game is being moved outside the Steam dir, create a symlink.

        :param curr_path: a string containing the current path of the game.
        :param dest_path: a string containing the destination path of the game.
        :create_symlink: True to create a symlink, otherwise False.
        :return: A string containing an error message if an error occurs, otherwise None.
        """
        if os.path.islink(dest_path) and create_symlink is False:
            os.rmdir(dest_path)

        if create_symlink is True:  # test to see if we can create a symlink
            td = tempfile.mktemp()
            try:
                os.symlink(td, r'c:\foo_123', True)
            except OSError as err:
                return 'Unable to create the symlink. \nPlease run this program as Administrator'
            else:
                os.rmdir(r'c:\foo_123')

        if os.path.exists(dest_path):
            fsize = util.get_folder_size(dest_path)
            if fsize == 0:
                try:
                    shutil.rmtree(dest_path)
                except IOError as err:
                    return 'The directory {} already exists and cannot be deleted!'.format(dest_path)
            else:
                return 'There is not enough space on {} to move the game!'.format(os.path.splitdrive(dest_path))

        try:
            shutil.move(curr_path, dest_path)
        except IOError as err:
            return 'An error occurred when attempting to move the game!'

        if create_symlink:
            os.symlink(dest_path, curr_path, True)
            return 'Moving complete!'

    def update_games(self):
        """Update the game list."""
        self._get_local_games()
        self._get_remote_games()

    def validate_paths(self):
        """
        Validate that the provided paths exist. If the remote dir does not exist,
        the user will be prompted to create it.
        """
        if not os.path.exists(self.steam_dir):
            print('\n The directory {} does not exist!\nThe program will now exit!'.format(self.steam_dir))
            sys.exit(-1)

        if not os.path.exists(self.remote_dir):
            print('\n The directory {} does not exist!\n'.format(self.remote_dir))
            choice = input('Shall I create it? (Y/N): ')
            if choice in ['y', 'Y']:
                try:
                    os.makedirs(self.remote_dir)
                except OSError as err:
                    print('The following error occurred when trying to create {}: '.format(self.remote_dir))
                    print(err)
                    sys.exit('The program will now exit.')
            else:
                sys.exit('The program will now exit.')

    def _get_local_games(self):
        """Get a list of the local games."""
        self.local_games = [dir for dir in os.listdir(self.steam_dir)
                            if os.path.isdir(os.path.join(self.steam_dir, dir)) and not
                            os.path.islink(os.path.join(self.steam_dir, dir))]

    def _get_remote_games(self):
        """Get a list of the remote games *linked* in the steam dir and a list of the games *installed there as well."""
        games = [dir for dir in os.listdir(self.steam_dir)
                 if os.path.isdir(os.path.join(self.steam_dir, dir)) and
                 os.path.islink(os.path.join(self.steam_dir, dir))]

        remote_games = [dir for dir in os.listdir(self.remote_dir)
                        if os.path.isdir(os.path.join(self.remote_dir, dir)) and dir not in games]

        self.remote_games = games
        self.remote_installed_games = remote_games
