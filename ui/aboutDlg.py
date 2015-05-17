# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Mon Aug 19 05:33:05 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_dlgAbout(object):
    def setupUi(self, dlgAbout):
        dlgAbout.setObjectName("dlgAbout")
        dlgAbout.setWindowModality(QtCore.Qt.WindowModal)
        dlgAbout.setEnabled(True)
        dlgAbout.resize(322, 114)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Steam.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgAbout.setWindowIcon(icon)
        self.textBrowser = QtGui.QTextBrowser(dlgAbout)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(20, 40, 281, 61))
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet("")
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.lblVersion = QtGui.QLabel(dlgAbout)
        self.lblVersion.setGeometry(QtCore.QRect(20, 20, 271, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.lblVersion.setFont(font)
        self.lblVersion.setObjectName("lblVersion")

        self.retranslateUi(dlgAbout)
        QtCore.QMetaObject.connectSlotsByName(dlgAbout)

    def retranslateUi(self, dlgAbout):
        dlgAbout.setWindowTitle(QtGui.QApplication.translate("dlgAbout", "About SteamMover", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("dlgAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">SteamMover: Created by Robin L. Siebler</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Inspired by </span><a href=\"http://www.traynier.com/software/steammover\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">Steam Mover</span></a><span style=\" font-size:8pt;\"> and </span><a href=\"http://www.stefanjones.ca/steam/\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">Steam Tool Library Manager</span></a><span style=\" font-size:8pt;\">.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVersion.setText(QtGui.QApplication.translate("dlgAbout", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

