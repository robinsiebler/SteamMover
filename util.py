# ------------------------------------------
# Name:     util.py
# Purpose:  utility functions
#
# Author:   Robin Siebler
# Created:  7/31/13
# ------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/31/13'

import os
import win32file
import winreg
from decimal import getcontext

import win32com.client as com


def get_folder_size(folder_path):
    """ Uses WSH to get the size of a folder. NOT THREAD SAFE!!!

    :param folder_path: a string containing a *valid* path
    :return: a float containing the size of the folder in MB
    """

    fso = com.Dispatch("Scripting.FileSystemObject")
    folder = fso.GetFolder(folder_path)
    MB = 1024*1024.0
    fsize = folder.Size/MB
    getcontext().prec = 4
    context = getcontext()
    return round(float(context.create_decimal(fsize)), 4)


def get_free_space(path):
    """
    Returns the number of free MB on the drive that the path is on.

    :param path: a string containing a path on the drive to check
    :return: a float containing the number of free MB
    """
    secsPerClus, bytesPerSec, nFreeClus, totClus = win32file.GetDiskFreeSpace(path)
    MB = 1024*1024.0
    fspace = (secsPerClus * bytesPerSec * nFreeClus) / MB
    getcontext().prec = 4
    context = getcontext()
    return round(float(context.create_decimal(fspace)), 2)


def get_steam_path():
    """Query the registry for the Steam Path.

    :return: The Steam path if found, otherwise None.
    """
    try:
        hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        value, type = winreg.QueryValueEx(hKey, "SteamPath")
    except WindowsError as err:
        return None

    steam_path = os.path.abspath(os.path.join(value, r'steamapps\common'))
    if os.path.exists(steam_path):
        return steam_path
    else:
        return None
