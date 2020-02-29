# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tpis.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(345, 213)
        Dialog.setMinimumSize(QtCore.QSize(345, 213))
        Dialog.setMaximumSize(QtCore.QSize(345, 213))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWindowOpacity(0.8)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(12, 20, 321, 141))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(131, 170, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Axure Handwriting")
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tips"))
        self.label.setText(_translate("Dialog", "小陈鸽"))
        self.pushButton.setText(_translate("Dialog", "完全O98K"))
