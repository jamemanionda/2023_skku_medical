import sys

import pydicom
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QMainWindow, QTreeWidgetItem, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QAction, QIcon, QPixmap, Qt
from qt_material import apply_stylesheet
from first_window_ui import Ui_Dialog

class FirstWindow(QMainWindow,Ui_Dialog):
    def __init__(self, parent=None, openAction=None):
        super(FirstWindow, self


              ).__init__(parent)
        self.main = QUiLoader().load('main.ui', self)
        self.setupUi(self)
        apply_stylesheet(self, 'light_pink.xml')
        self.setWindowTitle('DICOM')
        self.selectMenu()



    def selectMenu(self):
        self.comboBox.clear()
        self.comboBox.addItem('영상조회')
        self.comboBox.addItem('영상위변조조회')
        self.comboBox.addItem('영상위변조비교')
        self.comboBox.currentIndexChanged.connect(self.show_description)

        self.description_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.description_label)

        self.setLayout(layout)


    def show_description(self):
        selected_menu = self.comboBox.currentText()

        if selected_menu == "영상조회":
            picture_path = 'img/x-ray.png'
            description = "단일영상에 대한 기본정보를 확인합니다."
        elif selected_menu == "영상위변조조회":
            picture_path = 'img/fake.png'
            description = "단일영상에 대한 위변조분석을 진행합니다."
        elif selected_menu == "영상위변조비교":
            picture_path = 'img/3_compare.png'
            description = "두 영상에 대한 위변조 분석 및 비교를 진행합니다."
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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = FirstWindow()
    ex.show()
    sys.exit(app.exec())

