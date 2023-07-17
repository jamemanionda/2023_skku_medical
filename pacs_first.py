import sys

import pydicom
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QMainWindow, QTreeWidgetItem, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QAction, QIcon, QPixmap, Qt
from qt_material import apply_stylesheet
from first_window_ui import Ui_Dialog
from History_Timeline import History_Timeline
from PyQt5 import uic
class FirstWindow(QMainWindow,Ui_Dialog):
    def __init__(self, parent=None, openAction=None):
        super().__init__(parent)
        self.main = QUiLoader().load('first_window.ui', self)
        self.setupUi(self)
        apply_stylesheet(self, 'light_pink.xml')
        self.setWindowTitle('DICOM')
        self.selectMenu()



    def selectMenu(self):
        self.comboBox.clear()
        self.comboBox.addItem('DB 조회')
        self.comboBox.addItem('Log 조회')
        self.comboBox.addItem('History 조회')
        self.comboBox.currentIndexChanged.connect(self.show_description)

        self.description_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.description_label)

        self.setLayout(layout)


    def show_description(self):
        selected_menu = self.comboBox.currentText()

        if selected_menu == "DB 조회":
            picture_path = 'img/x-ray.png'
            description = "SQL 기록을 조회합니다."
        elif selected_menu == "Log 조회":
            picture_path = 'img/fake.png'
            description = "시스템 로그를 조회합니다."
        elif selected_menu == "History 조회":
            picture_path = 'img/3_compare.png'
            self.buttonBox.accepted.connect(self.on_accepted)
            description = "유저가 편집한 정보등의 기록을 조회합니다. "

        else:
            description = "선택하세요."

        # QLabel에 텍스트 설정
        pixmap = QPixmap(picture_path).scaled(500,500,Qt.KeepAspectRatio)
        self.descrip_pic.setScaledContents(True)
        self.descrip_pic.setPixmap(pixmap)
        self.label_description.setText(description)

    def onActivated(self, text):
        self.label.setText('영상위변조비교')
        self.label.adjustSize()

    @staticmethod
    def on_accepted():
        try:
            form_class = uic.loadUiType('History_Timeline.ui')[0]
            history_timeline_instance = History_Timeline(form_class)
            history_timeline_instance.show()
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = FirstWindow()
    ex.show()
    sys.exit(app.exec())
