# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'portError.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Error(object):
    def setupUi(self, Error):
        Error.setObjectName("Error")
        Error.resize(251, 143)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Error.sizePolicy().hasHeightForWidth())
        Error.setSizePolicy(sizePolicy)
        Error.setMinimumSize(QtCore.QSize(251, 143))
        Error.setMaximumSize(QtCore.QSize(251, 143))
        self.centralwidget = QtWidgets.QWidget(Error)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_ok = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ok.setGeometry(QtCore.QRect(70, 60, 101, 31))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        Error.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Error)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 251, 26))
        self.menubar.setObjectName("menubar")
        Error.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Error)
        self.statusbar.setObjectName("statusbar")
        Error.setStatusBar(self.statusbar)

        self.retranslateUi(Error)
        QtCore.QMetaObject.connectSlotsByName(Error)

    def retranslateUi(self, Error):
        _translate = QtCore.QCoreApplication.translate
        Error.setWindowTitle(_translate("Error", " "))
        self.pushButton_ok.setText(_translate("Error", "OK"))
        self.label.setText(_translate("Error", "Lütfen önce port açınız!"))

