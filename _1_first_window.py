import sys

import pydicom
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QMainWindow, QTreeWidgetItem
from PySide6.QtGui import QAction, QIcon
from qt_material import apply_stylesheet
from first_window_ui import Ui_Dialog

class FirstWindow(QMainWindow,Ui_Dialog):
    def __init__(self, parent=None, openAction=None):
        super(FirstWindow, self).__init__(parent)
        self.main = QUiLoader().load('main.ui', self)
        self.setupUi(self)
        apply_stylesheet(self, 'light_pink.xml')

        self.selectMenu()

    def selectMenu(self):
        self.comboBox.clear()
        self.comboBox.addItem('영상조회')
        self.comboBox.addItem('영상위변조비교')
        self.onActivated()

    def onActivated(self):

        if self.comboBox.currentText() == '영상위변조비교':
            self.label_description.setText('원본파일이 확보되었을때를 비교합니다.')
        elif self.comboBox.currentText() == '영상조회':
            self.label_description.setText('단순한 영상조회입니다..')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = FirstWindow()
    ex.show()
    app.exec()
