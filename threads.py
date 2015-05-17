# ------------------------------------------
# Name:     threads.py
# Purpose:  classes for managing threads
#
# Author:   Robin Siebler
# Created:  8/20/13
# ------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '8/20/13'

from PySide.QtCore import *  # necessary for threads


class WorkThread(QThread):
    """"Old style of thread management - http://joplaete.wordpress.com/2010/07/21/threading-with-pyqt4/"""
    def __init__(self):
        QThread.__init__(self)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()


class GenericThread(QThread):
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)


class WorkerThread(QObject):
    """new style of thread management. I got this class from
    http://www.verious.com/qa/how-to-move-an-object-back-and-forth-between-qthreads-in-pyqt/ """
    mainThread = QThread.currentThread()
    finished = Signal()
    doingWork = Signal(str)

    def __init__(self, function, *args, parent=None, **kwargs):
        super(WorkerThread, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def doWork(self):
        self.doingWork.emit('Moving files...')
        if self.kwargs:
            self.function(self.args, self.kwargs)
        else:
            self.function(self.args)
        self.moveToThread(self.mainThread)
        self.doingWork.emit('Task complete!')
        self.finished.emit()
