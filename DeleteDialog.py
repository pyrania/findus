# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './DeleteDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.setEnabled(True)
        Dialog.resize(290, 98)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(290, 98))
        Dialog.setMaximumSize(QtCore.QSize(290, 98))
        Dialog.setWindowTitle("")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15, 23, 251, 16))
        self.label.setMinimumSize(QtCore.QSize(251, 16))
        self.label.setMaximumSize(QtCore.QSize(251, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.bOK = QtWidgets.QPushButton(Dialog)
        self.bOK.setGeometry(QtCore.QRect(200, 60, 81, 32))
        self.bOK.setDefault(True)
        self.bOK.setFlat(False)
        self.bOK.setObjectName("bOK")
        self.bCancel = QtWidgets.QPushButton(Dialog)
        self.bCancel.setGeometry(QtCore.QRect(90, 60, 113, 32))
        self.bCancel.setObjectName("bCancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "Ausgewählte Daten wirklich löschen?"))
        self.bOK.setText(_translate("Dialog", "Ok"))
        self.bCancel.setText(_translate("Dialog", "Abbrechen"))

