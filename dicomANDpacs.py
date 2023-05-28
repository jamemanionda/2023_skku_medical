"""
 2023.02.23 # 박재현
 수정1차 : DICOM 분석
 수정3차 : DICOM Tag 주석으로 추가
 수정4차 : UI 출력을 위한 Form 클래스 추가, DicomInformation.output_dicom_data 함수에 Form 클래스 삽입, Form UI 크기 조절 필요
 #이은지
 수정 2차 : GUI 연결(pyside import 추가,
"""
import sys

import dicom as dicom
#pip install pydicom

import pydicom
import os
import sys


from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import report
from qt_material import apply_stylesheet
from PyQt5 import uic
#from mainui import Ui_MainWindow
import _5_metadata
form_class = uic.loadUiType("dicomANDpacs.ui")[0]
class dicomandpacsmain(QMainWindow, form_class):

    def __init__(self):


        #UI 설정
        super().__init__()
        #super(single_DicomInformation, self).__init__(parent)

        self.setupUi(self)
        #apply_stylesheet(self, 'light_pink.xml')
        self.dicom_filepath = ''
        self.dicom_filename = ''
        self.addressip = '192.168.0.1'
        self.fname = 'hello'
        #메인 기능
        #self.mainfunction()

        self.pushButton.clicked.connect(lambda: self.makeReport())
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
            self.realpath = report.make_docx(self.addressip, self.fname, self.fname)
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
            path = current + '/'+self.realpath
            os.startfile(path)

    #dicom파일 데이터 획득
    #def get_dicom_data(self):


    #dicom파일 데이터 출력

    #def get_pacs_data(self):




    #def tagview(self):





if __name__ == '__main__':
    #app = QApplication(sys.argv)
    app = QApplication(sys.argv)

    ex = dicomandpacsmain()


    ex.show()

    app.exec()
