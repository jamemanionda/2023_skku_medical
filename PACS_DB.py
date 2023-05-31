# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PACS_DB.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 452)
        self.DBcolumn_comboBox = QtWidgets.QComboBox(Dialog)
        self.DBcolumn_comboBox.setGeometry(QtCore.QRect(20, 10, 181, 21))
        self.DBcolumn_comboBox.setObjectName("DBcolumn_comboBox")
        self.DatabaseTable = QtWidgets.QTableView(Dialog)
        self.DatabaseTable.setGeometry(QtCore.QRect(20, 40, 601, 391))
        self.DatabaseTable.setObjectName("DatabaseTable")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

