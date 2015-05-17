# ------------------------------------------
# Name:     main.pyw (GUI)
# Purpose:  SteamMover will list all of the directories (games) under the steam Common dir. The user can select
#           a game and it will be moved to the directory specified as the Remote directory. A symbolic link
#           will be created to the original directory so that Steam will still launch the game.
#
# Author:   Robin Siebler
# Created:  7/31/13
# ------------------------------------------

# TODO: why do I have to edit mainGUI.py in order to correctly import icons_rc w/Python 3?
# TODO: implement logging?


__author__ = 'Robin Siebler'
__date__ = '7/31/13'

__appname__ = 'SteamMover'
__module__ = 'main'
__version__ = '1.0'
__rel_date__ = '8/21/13'

from PySide.QtCore import *  # Required for the UI
from PySide.QtGui import *  # Required for the UI

from decimal import getcontext  # Used to control the number of decimal places
from fsize import FolderSize  # Thread-safe means of getting the directory size
from games import Games  # Game Class
from threads import WorkerThread  # Threading class
from ui import mainGui  # Main UI
from ui import aboutDlg  # About dialog
from ui import legendDlg  # Legend  - meaning of the icons

# import logging
import os
import shutil  # Used to move files
import sys
import tempfile  # Used to verify the ability to create symlinks
import util  # Helper functions

# Path for the INI file
appDataPath = os.path.join(os.environ['APPDATA'] + 'SteamMover')
if not os.path.exists(appDataPath):
	try:
		os.mkdir(appDataPath)
	except (OSError, IOError) as err:
		appDataPath = os.getcwd()

# Path for the log file
# logging.basicConfig(filename=appDataPath + 'SteamMover.log',
#                     format='%(asctime)-15s: %(name)-18s - %(levelname)-8s -\
#                      %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s')
# logger = logging.getLogger(name='main-gui')


class MainWindow(QMainWindow, mainGui.Ui_MainWindow):
	"""The main UI window."""

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)

		# Application icon
		self.setWindowIcon(QIcon(':/icons/Steam.ico'))

		# Create the taskbar icon
		if os.name == 'nt':
			# This is needed to display the app icon on the taskbar on Windows 7
			import ctypes

			myappid = 'MyOrganization.MyGui.1.0.0'  # arbitrary string
			ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

		# Instance variables
		self.settings = None
		self.missing_steam_dir = False
		self.missing_remote_dir = False
		self.read_settings()

		# Initial control state
		self.progressBar.setVisible(False)
		self.lbl_Progress.setVisible(False)
		self.btnMovetoStorage.setEnabled(False)
		self.btnMovetoSteam.setEnabled(False)

		# Validate the Steam directory
		if self.SteamDir is None:
			self.SteamDir = util.get_steam_path()
			if self.SteamDir is None:
				self.missing_steam_dir = True

		# Validate the remote directory
		if self.RemoteDir is None or not os.path.exists(self.RemoteDir):
			self.missing_remote_dir = True

		# Prompt the user to select the Remote directory
		if self.missing_steam_dir or self.missing_remote_dir:
			if self.missing_steam_dir:
				QMessageBox.warning(None, 'Error!', 'Unable to locate the Steam Directory. '
				                                    'You will now be prompted to select it.')
				self.get_steam_dir()
			if self.missing_remote_dir:
				self.lbl_FreeRemote.setVisible(False)
				self.lbl_FreeSteam.setVisible(False)
				self.show()
				QMessageBox.information(None, 'First Launch', 'You appear to be launching the app for the 1st ' +
				                        'time.\n\nYou will now be prompted to select a remote folder for\n' +
				                        ' storing Steam games.')
				self.get_remote_dir()
				self.lbl_FreeRemote.setVisible(True)
				self.lbl_FreeSteam.setVisible(True)

			self.update_controls()
			self.write_settings()
		else:
			self.update_controls()

		# Connect signals and slots
		self.btnRefresh.clicked.connect(self.refresh_data)
		self.btnBrowse.clicked.connect(self.update_remote)
		self.action_About.triggered.connect(self.show_about)
		self.action_Exit.triggered.connect(self.close_event)
		self.action_Legend.triggered.connect(self.show_legend)
		self.btnMovetoSteam.clicked.connect(self.move_to_steam)
		self.btnMovetoStorage.clicked.connect(self.move_to_storage)
		self.treeGames.itemSelectionChanged.connect(self.item_selected)

	def close_event(self):
		"""Write the settings and exit."""
		self.write_settings()
		self.close()

	def get_remote_dir(self):
		"""Display a dialog so the user can select the Remote Directory."""
		flags = QFileDialog.ShowDirsOnly
		result = QFileDialog.getExistingDirectory(self, 'Browse for a remote directory for games:', os.getcwd(), flags)
		if result == '' and self.RemoteDir is not None:  # if the user pressed "Cancel" and the Remote dir is valid
			self.missing_remote_dir = False
			return
		elif result != '':
			self.missing_remote_dir = False
			self.RemoteDir = result
			self.lneRemoteDir.setText(self.RemoteDir)
			self.write_settings()
		else:
			QMessageBox.critical(None, 'Fatal Error', 'You failed to select a remote storage directory.\n'
			                                          'The program will now exit!')
			sys.exit()

	def get_steam_dir(self):
		"""Display a dialog so the user can select the Steam Directory."""
		flags = QFileDialog.ShowDirsOnly
		result = QFileDialog.getExistingDirectory(self, 'Browse for the Steam Directory:', os.getcwd(), flags)

		if result != '':
			self.SteamDir = result
		else:
			QMessageBox.critical(None, 'Fatal Error', 'You failed to select the Steam Directory.\n'
			                                          'The program will now exit!')
			sys.exit()

	def item_selected(self):
		"""Enable/Disable Move buttons based upon selected item."""
		location = self.treeGames.currentItem().text(1)
		if location == 'Steam Folder':
			self.btnMovetoStorage.setEnabled(True)
			self.btnMovetoSteam.setEnabled(False)
		elif location == 'Remote Folder':
			self.btnMovetoStorage.setEnabled(False)
			self.btnMovetoSteam.setEnabled(True)
		else:
			self.btnMovetoStorage.setEnabled(False)
			self.btnMovetoSteam.setEnabled(False)

	def move_game(self, curr_path, dest_path, create_symlink=False):
		"""
		Move a game from the current folder to the destination folder.

		:param curr_path: a string containing the current path for the game.
		:param dest_path: a string containing the destination path for the game.
		:param create_symlink: True to create a symlink, otherwise False.
		"""

		self.btnMovetoStorage.setEnabled(False)
		self.btnMovetoSteam.setEnabled(False)
		self.treeGames.setEnabled(False)

		# Make sure there is enough free space for the move
		game_size = util.get_folder_size(curr_path)
		free_space = util.get_free_space(os.path.split(dest_path)[0])
		if free_space - game_size < 10:
			QMessageBox.Critical(None, 'Unable to move game!', 'There is not enough free space to move the game!')
		else:

			result = self._move_game(curr_path, dest_path, create_symlink)
			# I could not figure out how to use the code that already existed in this class with threads. :(
			# result = self.games.move_game(curr_path, dest_path, create_symlink)
			if result:
				QMessageBox.critical(None, 'Critical Error!', result)

	def move_to_steam(self):
		""""Move a game to the Steam directory."""
		game = self.treeGames.currentItem().text(0)
		self.statusbar.showMessage('Now copying ' + game + ' to the Steam directory')
		curr_path = self.treeGames.currentItem().child(0).text(1)
		dest_path = os.path.join(self.SteamDir, game)
		self.move_game(curr_path, dest_path)

	def move_to_storage(self):
		"""Move a game to the Remote directory."""
		game = self.treeGames.currentItem().text(0)
		self.statusbar.showMessage('Now copying ' + game + ' to the Remote directory')
		curr_path = self.treeGames.currentItem().child(0).text(1)
		dest_path = os.path.join(self.RemoteDir, game)
		self.move_game(curr_path, dest_path, True)

	def read_settings(self):
		"""Read the settings from the INI file."""
		self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'Robins_Apps', 'SteamMover')
		self.settings.beginGroup('Paths')
		self.SteamDir = (self.settings.value('SteamPath'))
		self.RemoteDir = (self.settings.value('RemotePath'))
		self.settings.endGroup()

	def refresh_data(self):
		"""Refresh the TreeView after the Refresh button is clicked or the Remote Dir changes."""
		self.games.remote_dir = self.RemoteDir
		self.games.update_games()
		self.game_list = sorted(list(self.games.local_games + self.games.remote_games +
		                             self.games.remote_installed_games), key=lambda x: x.lower())
		self.treeGames.clear()
		items = []
		for game in self.game_list:
			if game in self.games.local_games:
				game_path = os.path.join(self.SteamDir, game)
			elif game in self.games.remote_games:
				game_path = os.readlink(os.path.join(self.SteamDir, game))
			elif game in self.games.remote_installed_games:
				game_path = os.path.join(self.RemoteDir, game)
			# game_size = util.get_folder_size(game_path)
			# I am using this function to get the folder size instead of the util module function
			# because that function is not thread-safe and I didn't know how to fix it.
			fsize = FolderSize()
			fsize.searchPath(game_path)
			# convert the folder size to MB and restrict the number of decimal places
			MB = 1024 * 1024.0
			game_size = fsize.totalSize / MB
			getcontext().prec = 4
			context = getcontext()
			game_size = round(float(context.create_decimal(game_size)), 4)

			if game in self.games.local_games:
				location = 'Steam Folder'
			elif game in self.games.remote_games:
				location = 'Remote Folder'
			elif game in self.games.remote_installed_games:
				game_path = os.path.join(self.RemoteDir, game)
				location = 'Installed into Remote Steam Folder'
			item = QTreeWidgetItem(None, [game, location, str(game_size)])
			item.addChild(QTreeWidgetItem(None, ['', game_path]))
			if game in self.games.local_games:
				item.setIcon(0, QIcon(':/icons/backward.ico'))
			elif game in self.games.remote_games:
				item.setIcon(0, QIcon(':/icons/forward.ico'))
			elif game in self.games.remote_installed_games:
				item.setIcon(0, QIcon(':/icons/g5_vpc_drive.ico'))
			items.append(item)
		self.treeGames.insertTopLevelItems(len(self.game_list), items)

	def show_about(self):
		"""Display the About dialog."""

		class AboutDialog(QDialog, aboutDlg.Ui_dlgAbout):
			def __init__(self, parent=None):
				super(AboutDialog, self).__init__(parent)
				self.setupUi(self)

		adlg = AboutDialog(self)
		adlg.lblVersion.setText('Steam Mover version ' + __version__ + ' (' + __rel_date__ + ')')
		adlg.show()

	def show_legend(self):
		"""Display the Legend dialog."""

		class LegendDialog(QDialog, legendDlg.Ui_dlgLegend):
			def __init__(self, parent=None):
				super(LegendDialog, self).__init__(parent)
				self.setupUi(self)

		ldlg = LegendDialog(self)
		ldlg.show()

	def show_progress_bar(self):
		"""Display the progress bar"""
		self.lbl_Progress.setVisible(True)
		self.progressBar.show()

	def update_controls(self):
		"""Finish updating the contents of the controls after basic validation."""
		self.lneSteamDir.setText(self.SteamDir)
		self.lneRemoteDir.setText(self.RemoteDir)
		self.lbl_FreeSteam.setText('Free Space on Steam Drive is: ' +
		                           str(util.get_free_space(self.SteamDir)) + ' MB')
		self.lbl_FreeRemote.setText('Free Space on Remote Drive is: ' +
		                            str(util.get_free_space(self.RemoteDir)) + ' MB')
		self.treeGames.setColumnWidth(0, 425)
		self.treeGames.setColumnWidth(1, 425)
		self.games = Games(self.SteamDir, self.RemoteDir)
		self.games.update_games()
		self.refresh_data()

	def update_ui(self, text):
		"""Update the UI after a game is moved."""
		self.lbl_Progress.setVisible(False)
		self.progressBar.close()
		self.statusbar.showMessage(text)
		self.refresh_data()
		self.treeGames.setEnabled(True)

	def update_remote(self):
		"""Update the game data with info from the new Remote directory."""
		self.get_remote_dir()
		self.refresh_data()

	def write_settings(self):
		"""Write the INI settings to a file."""
		self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'Robins_Apps', 'SteamMover')
		self.settings.beginGroup('Paths')
		self.settings.setValue('SteamPath', self.SteamDir)
		self.settings.setValue('RemotePath', self.RemoteDir)
		self.settings.endGroup()

	def _move_files(self, args):
		"""Move the files. This function will be called from a thread so the UI remains responsive."""
		curr_path, dest_path, create_symlink = args
		try:
			shutil.move(curr_path, dest_path)
		except IOError as err:
			return 'An error occurred when attempting to move the game!'

		if create_symlink:
			os.symlink(dest_path, curr_path, True)
			self.emit(SIGNAL("update_ui(QString)"), 'Files moved!')

	def _move_game(self, curr_path, dest_path, create_symlink=False):
		"""
		Move a game from the current dir to the destination dir.
		If the game is being moved outside the Steam dir, create a symlink.
		The actual move operation will occur within a thread.

		:param curr_path: a string containing the current path of the game.
		:param dest_path: a string containing the destination path of the game.
		:create_symlink: True to create a symlink, otherwise False.
		:return: A string containing an error message if an error occurs, otherwise None.
		"""

		# If the destination path is a symlink AND we don't need one, remove it.
		if os.path.islink(dest_path) and create_symlink is False:
			os.rmdir(dest_path)

		# Test to see if we can create a symlink
		if create_symlink is True:
			td = tempfile.mktemp()
			try:
				# The string is a filename that SHOULD never exist on  a normal system
				os.symlink(td, r'c:\foo_123',True)
			except OSError as err:
				return 'Unable to create the symlink. \nPlease run this program as Administrator'
			else:
				os.rmdir(r'c:\foo_123')

		# If the destination path exists AND is 0 bytes, try to remove it. Otherwise, bail.
		if os.path.exists(dest_path):
			fsize = util.get_folder_size(dest_path)
			if fsize == 0:
				try:
					shutil.rmtree(dest_path)
				except IOError as err:
					return 'The directory {} already exists and cannot be deleted!'.format(dest_path)
			else:
				return 'There is not enough space on {} to move the game!'.format(os.path.splitdrive(dest_path))

		# Create the thread for moving the files
		self.obj = WorkerThread(self._move_files, curr_path, dest_path, create_symlink)
		self.thread = QThread()
		self.obj.moveToThread(self.thread)
		self.thread.started.connect(self.obj.doWork)
		self.obj.doingWork.connect(self.show_progress_bar)
		self.obj.finished.connect(self.killThread)
		self.thread.start()

	def killThread(self):
		"""Kill the thread once we are done with it."""
		self.thread.quit()
		self.thread.wait()
		self.obj.finished.disconnect()
		self.update_ui('Move operation complete!')


def main():
	"""Create the application window."""
	QCoreApplication.setApplicationName(__appname__)
	QCoreApplication.setApplicationVersion(__version__)
	QCoreApplication.setOrganizationName('Robins_Apps')

	app = QApplication(sys.argv)
	form = MainWindow()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()
