# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'legend.ui'
#
# Created: Thu Aug 15 23:27:35 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_dlgLegend(object):
    def setupUi(self, dlgLegend):
        dlgLegend.setObjectName("dlgLegend")
        dlgLegend.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgLegend.resize(400, 247)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Steam.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgLegend.setWindowIcon(icon)
        self.label = QtGui.QLabel(dlgLegend)
        self.label.setGeometry(QtCore.QRect(20, 30, 81, 61))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/backward.ico"))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(dlgLegend)
        self.label_2.setGeometry(QtCore.QRect(110, 50, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(dlgLegend)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 81, 61))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/forward.ico"))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(dlgLegend)
        self.label_4.setGeometry(QtCore.QRect(110, 120, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(dlgLegend)
        self.label_5.setGeometry(QtCore.QRect(20, 170, 81, 61))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/icons/g5_vpc_drive.ico"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(dlgLegend)
        self.label_6.setGeometry(QtCore.QRect(110, 190, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(dlgLegend)
        QtCore.QMetaObject.connectSlotsByName(dlgLegend)

    def retranslateUi(self, dlgLegend):
        dlgLegend.setWindowTitle(QtGui.QApplication.translate("dlgLegend", "Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgLegend", "Game Stored in Steam Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgLegend", "Game Stored in Remote Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("dlgLegend", "Game Installed in Remote Directory", None, QtGui.QApplication.UnicodeUTF8))

