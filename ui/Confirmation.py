# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirmation.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_confirmation(object):
    def setupUi(self, confirmation):
        confirmation.setObjectName("confirmation")
        confirmation.resize(259, 176)
        self.confim = QtWidgets.QPushButton(confirmation)
        self.confim.setGeometry(QtCore.QRect(140, 120, 90, 28))
        self.confim.setStyleSheet("background-color: rgb(13, 112, 6);")
        self.confim.setObjectName("confim")
        self.unconfirm = QtWidgets.QPushButton(confirmation)
        self.unconfirm.setGeometry(QtCore.QRect(30, 120, 90, 28))
        self.unconfirm.setStyleSheet("background-color: rgb(255, 0, 4);")
        self.unconfirm.setObjectName("unconfirm")
        self.label = QtWidgets.QLabel(confirmation)
        self.label.setGeometry(QtCore.QRect(200, 20, 31, 31))
        self.label.setStyleSheet("font: 57 12pt \"Ubuntu\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(confirmation)
        self.label_2.setGeometry(QtCore.QRect(80, 70, 151, 31))
        self.label_2.setStyleSheet("font: 57 12pt \"Ubuntu\";")
        self.label_2.setObjectName("label_2")
        self.name = QtWidgets.QLabel(confirmation)
        self.name.setGeometry(QtCore.QRect(20, 20, 181, 31))
        self.name.setStyleSheet("font: 57 12pt \"Ubuntu\";")
        self.name.setText("")
        self.name.setObjectName("name")

        self.retranslateUi(confirmation)
        QtCore.QMetaObject.connectSlotsByName(confirmation)

    def retranslateUi(self, confirmation):
        _translate = QtCore.QCoreApplication.translate
        confirmation.setWindowTitle(_translate("confirmation", "Dialog"))
        self.confim.setText(_translate("confirmation", "تایید"))
        self.unconfirm.setText(_translate("confirmation", "رد"))
        self.label.setText(_translate("confirmation", "نام : "))
        self.label_2.setText(_translate("confirmation", "آیا مطمعا هستید؟"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    confirmation = QtWidgets.QDialog()
    ui = Ui_confirmation()
    ui.setupUi(confirmation)
    confirmation.show()
    sys.exit(app.exec_())

