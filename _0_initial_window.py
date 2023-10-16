import os
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMessageBox, QApplication

import report2
from dicom_main2 import DicomInformation
from pacs_main import Pacs_main
from qt_material import apply_stylesheet

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        pacs_button = QPushButton('PACS', self)
        pacs_button.clicked.connect(self.pacsClicked)

        dicom_button = QPushButton('DICOM', self)
        dicom_button.clicked.connect(self.dicomClicked)

        self.report_button = QPushButton('Report', self)

        self.report_button.clicked.connect(lambda: self.makeReport())

        hbox = QHBoxLayout()
        hbox.addWidget(pacs_button)
        hbox.addWidget(dicom_button)

        self.setLayout(hbox)

        self.setWindowTitle('PACS vs. DICOM')
        self.setGeometry(300, 300, 300, 100)
        self.closeEvent = self.handleCloseEvent


    def pacsClicked(self):
        print('PACS button clicked')
        try:
            self.b = Pacs_main()  # aaaaa 클래스의 인스턴스 생성
            self.b.show()  # 생성된 인스턴스의 show() 메소드 호출

            return self.b
        except Exception as e:
            print(f"Error occurred: {e}")

    def dicomClicked(self):
        print('DICOM button clicked')
        try:
            self.a = DicomInformation()  # aaaaa 클래스의 인스턴스 생성
            self.a.show()  # 생성된 인스턴스의 show() 메소드 호출

            return self.a
        except Exception as e:
            print(f"Error occurred: {e}")



    def handleCloseEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def makeReport(self):
        self.show_popup_ok('report', '보고서를 만드시겠습니까?')
    def show_popup_ok(self, title: str, content: str):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setStyleSheet('font: 25 11pt "KoPubWorldDotum";background-color: rgb(255, 255, 255);')
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.realpath = report2.make_docx(self.a, self.b)
            self.open_file('report', '보고서를 열어보시겠습니까?')

    def open_file(self, title: str, content: str):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setStyleSheet('font: 25 11pt "KoPubWorldDotum";background-color: rgb(255, 255, 255);')
        result = msg.exec_()
        if result == QMessageBox.Ok:
            current = os.getcwd()
            path = self.realpath
            os.startfile(path)

class aaaaa(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('aaaaa')
        self.setGeometry(400, 400, 300, 200)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec()
