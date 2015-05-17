# ------------------------------------------
# Name:     ${NAME}
# Purpose:  
#
# Author:   Robin Siebler
# Created:  8/23/13
# ------------------------------------------
from unittest import TestCase
from games import Games
import util
import os

__author__ = 'Robin Siebler'
__date__ = '8/23/13'

# TODO: create dummy test dir for steam and remote 'games'. Don't forget to include symlinks

steam_dir = r'f:\scripts\Python\Practice\PyQt\SteamMover\_test_data\steam_dir'
remote_dir = r'f:\scripts\Python\Practice\PyQt\SteamMover\_test_data\remote_dir'
curr_path = r'f:\scripts\Python\Practice\PyQt\SteamMover\_test_data\steam_dir\bastion'
dest_path = r'f:\scripts\Python\Practice\PyQt\SteamMover\_test_data\remote_dir\bastion'
r_delete_me = r'f:\scripts\Python\Practice\PyQt\SteamMover\_test_data\remote_dir\delete_me'
s_delete_me = r'f:\scripts\Python\Practice\PyQt\SteamMover\_test_data\steam_dir\delete_me'

# steam_dir = r'e:\SteamMover\_test_data\steam_dir'
# remote_dir = r'e:\SteamMover\_test_data\remote_dir'
# curr_path = r'e:\SteamMover\_test_data\steam_dir\bastion'
# dest_path = r'e:\SteamMover\_test_data\remote_dir\bastion'
# r_delete_me = r'e:\SteamMover\_test_data\remote_dir\delete_me'
# s_delete_me = r'e:\SteamMover\_test_data\steam_dir\delete_me'

local_games = ['bastion',
               'bionic commando',
               'blur',
               'brain spa',
               'call of duty',
               'capsized',
               'cloning clyde',
               'crysis',
               'dead space',
               'defensegridtheawakening',
               'deus ex - human revolution',
               'diamond dan',
               'disciples 3',
               'Dishonored',
               'divinity ii - dragon knight saga',
               ]
remote_games = ['Alan Wake',
                'anomaly warzone earth',
                'ares',
                "Assassin's Creed Brotherhood",
                "Assassin's Creed Revelations"
                ]
remote_installed_games = ['alan wakes american nightmare',
                          "Assassin's Creed 3",
                          "Baldur's Gate Enhanced Edition",
                          'Batman Arkham City GOTY',
                          'Bejeweled 3',
                          'BioShock Infinite',
                          'Dark Souls Prepare to Die Edition',
                          'Dungeons - The Dark Lord',
                          'Eador. Masters of the Broken World',
                          'Hitman Absolution',
                          'mark_of_the_ninja',
                          'Skyrim',
                          'Tomb Raider'
                          ]


class TestGames(TestCase):
    def setUp(self):
        self.g = Games(steam_dir, remote_dir)
        self.g._get_local_games()
        self.g._get_remote_games()

    def test_num_local_games(self):
        self.assertEqual(len(self.g.local_games), 15)

    def test_num_remote_games(self):
        self.assertEqual(len(self.g.remote_games), 5)

    def test_num_remote_installed_games(self):
        self.assertEqual(len(self.g.remote_installed_games), 13)

    def test_list_local_games(self):
        self.assertListEqual(self.g.local_games, local_games)

    def test_list_remote_games(self):
        self.assertListEqual(self.g.remote_games, remote_games)

    def test_list_remote_installed_games(self):
        self.assertListEqual(self.g.remote_installed_games, remote_installed_games)

    def test_move_game_path_exists(self):  # test lines 48 - 52 of games.move_game()
        # setup
        os.mkdir(r_delete_me)
        os.mkdir(s_delete_me)
        result = self.g.move_game(r_delete_me, s_delete_me, True)
        self.assertTrue(result == 'Moving complete!' and os.path.islink(r_delete_me))
        # tear down
        os.rmdir(r_delete_me)
        os.rmdir(s_delete_me)

    def test_move_to_remote(self):
        self.g.move_game(curr_path, dest_path, True)
        self.g.update_games()
        self.assertEqual(len(self.g.local_games), 14)
        self.assertEqual(len(self.g.remote_games), 6)

    def test_move_to_steam(self):
        self.g.move_game(dest_path, curr_path)
        self.g.update_games()
        self.assertEqual(len(self.g.local_games), 15)
        self.assertEqual(len(self.g.remote_games), 5)

    def test_validate_paths(self):
        self.g.validate_paths()


class TestUtil(TestCase):
    def test_get_folder_size(self):
        self.assertEqual(util.get_folder_size(r'.\imageformats'), 2.264)

    def test_get_free_space(self):
        # this test will have to be adjusted for drive letter and free space
        # self.assertEqual(util.get_free_space(r'e:'), 30020.0)
        self.assertEqual(util.get_free_space(r'e:'), 69270.0)

    def test_get_steam_path(self):
        self.assertEqual(util.get_steam_path(), 'e:\\program files (x86)\\steam\\steamapps\\common')
