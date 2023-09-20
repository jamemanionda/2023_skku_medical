"""
 2023.02.23 # 박재현
 수정1차 : DICOM 분석
 수정3차 : DICOM Tag 주석으로 추가
 수정4차 : UI 출력을 위한 Form 클래스 추가, DicomInformation.output_dicom_data 함수에 Form 클래스 삽입, Form UI 크기 조절 필요
 #이은지
 수정 2차 : GUI 연결(pyside import 추가,
"""
import glob
import sys

#import dicom as dicom
import pandas as pd
#pip install pydicom

import pydicom
import os
import sys
import PACS_log

from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PyQt5.QtCore import Qt
import report
from qt_material import apply_stylesheet
from PyQt5 import uic
#from mainui import Ui_MainWindow

form_class = uic.loadUiType("dicomANDpacs.ui")[0]
class Institution_1():
    def __init__(self, dcm):
        self.institution_name = str(dcm.get("InstitutionName"))  # 병원 이름
        self.institution_address = str(dcm.get("InstitutionAddress"))  # 병원 주소
        self.file_meta_information_version = str(dcm.file_meta.get("FileMetaInformationVersion"))  # filemeta 버전
        self.media_storage_sop_class_uid = str(dcm.file_meta.get("MediaStorageSOPClassUID"))  # SOP class UID
        self.media_storage_sop_instance_uid = str(dcm.file_meta.get("MediaStorageSOPInstanceUID"))  # SOP instance UID

class Patient_1():
    def __init__(self, dcm):
        self.patient_name = str(dcm.get("PatientName"))  # 환자 이름
        self.patient_id = str(dcm.get("PatientID"))  # 환자 ID
        self.patient_sex = str(dcm.get("PatientSex"))  # 환자 성별
        self.patient_birthday = str(dcm.get("PatientBirthDate"))  # 환자 생년월일
        self.patient_age = str(dcm.get("PatientAge"))  # 환자 나이
        self.patient_height = str(dcm.get("PatientSize"))  # 환자 키
        self.patient_weight = str(dcm.get("PatientWeight"))  # 환자 몸무게
        self.series_date = str(dcm.get("SeriesDate"))  # 진료 시작 날짜(추정)
        # 이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능
        self.performing_physician_name = str(dcm.get("PerformingPhysicianName"))  # 주치의
class dicomandpacsmain(QMainWindow, form_class):
    def __init__(self):
        #super(single_DicomInformation, self).__init__(parent)
        self.dicom_filepath = []
        self.dicom_filename = []
        self.Qlist = QListWidget()

        super().__init__()
        self.setupUi(self)
        #apply_stylesheet(self, 'light_pink.xml')
        self.addressip = '192.168.0.1'
        #self.fname = 'hello'
        #메인 기능
        #self.mainfunction()
        self.update_dcmlist(self.dicom_filename)
        self.pushButton.clicked.connect(lambda: self.makeReport())
        self.dcmlist.itemClicked.connect(self.dcmlistClicked)

    def makeReport(self):
        self.show_popup_ok('report', '보고서를 만드시겠습니까?')

    def update_dcmlist(self, list):
        for i, file in enumerate(list):
            self.dcmlist.addItem(QListWidgetItem(os.path.basename(file)))
            self.dicom_filepath.append(file)

    def show_popup_ok(self, title: str, content: str):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setStyleSheet('font: 25 11pt "KoPubWorldDotum";background-color: rgb(255, 255, 255);')
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.realpath = report.make_docx(self.addressip, self.file, self.file)
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

    def dcmlistClicked(self, item):
        self.tagtree.clear()
        self.fileinfotree.clear()
        self.filenum = self.dcmlist.currentRow()

        self.file = self.dicom_filepath[self.filenum]

        data, dcm, patient = self.get_dicom_data(self.file)
        self.tagview2(data, self.tagtree, dcm)
        self.fileview(self.file, self.fileinfotree)

        self.dicomExtract(str(self.dcmlist.currentItem()), patient)



    def get_dicom_data(self, file):
        dcm = pydicom.dcmread(str(file))
        dicom_filename = os.path.basename(file)

        # 파일 데이터


        # 환자 데이터
        patient1 = Patient_1(dcm)

        # 병원 데이터
        institution1 = Institution_1(dcm)

        data = self.tagview(file, patient1, institution1)
        return data, dcm, patient1







    def tagview(self, file, patient, institution): #0322
        data = [
            {"type": "File",
             "objects": [("File name", file), ("File Meta Information Version", institution.file_meta_information_version),
                         ("Media Storage SOP Class UID", institution.media_storage_sop_class_uid), ("Media Storage SOP Instance UID", institution.media_storage_sop_instance_uid)]},
            {"type": "Patient",
             "objects": [("Patient Name", patient.patient_name), ("Patient ID", patient.patient_id),
                         ("Patient Sex", patient.patient_sex), ("Patient Birthday", patient.patient_birthday),
                         ("Patient Age", patient.patient_age), ("Patient Height", patient.patient_height),
                         ("Patient Weight", patient.patient_weight), ("Series Date", patient.series_date),
                         ("Performing Physician's Name", patient.performing_physician_name)]},
            {"type": "Institution",
             "objects": [("Institution Name", institution.institution_name),
                         ("Institution Address", institution.institution_address)]},
        ]

        return data

    def tagview2(self, data, treeWidget, dcm):  # 0322
        for d in data:
            parent = self.add_tree_root(d['type'], "", treeWidget)
            for child in d['objects']:
                self.add_tree_child(parent, *child)

        from PyQt5.QtGui import QImage


        #self.display_video_in_dicom_view()



    def add_tree_root(self, name: str, description: str, treewidget):
        item = QTreeWidgetItem(treewidget)
        item.setText(0, name)
        item.setText(1, description)
        return item

    def add_tree_child(self, parent: QTreeWidgetItem, name: str, description: str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, description)
        parent.addChild(item)
        return item

    def dicomExtract(self, item, patient):
        self.viewrexlog_dataframe = pd.DataFrame(columns=['Time', 'Action', 'Explaination'])
        self.index = 0
        if True:        #Default 경로가 아닌 다른 경로에 파일이 저장되어 있을 경우, 조건문 추가 필요
            self.viewrexlogfile_folder = 'C:\\Users\\skku-dfl\\OneDrive - 성균관대학교\\문서\\SKKU_DFL\\DICOM\\Log'    #실제 로그파일의 폴더를 받을 수 있도록 변경할 것
        self.viewrexlogfile_path = self.viewrexlogfile_folder + "\\ViewRex.exe_*.log"
        textline = []
        for logfile in glob.glob(self.viewrexlogfile_path):
            filename = os.path.basename(logfile)
            with open(logfile, 'r', encoding='UTF-8') as file:
                for line in file:
                    textline.append(line)
                    if line == '\n':
                        for i in range(len(textline)-1):
                            textline[i] = textline[i].strip()
                        line = ' '.join(textline)
                        textline = []
                        text = line.split(' ', 4)
                        if len(text) <= 4:
                            continue
                        if text[0] != '':
                            if text[1] == '오후':
                                text[1] = 'PM'
                            elif text[1] == '오전':
                                text[1] = 'AM'

                            Time = text[0] + ' ' + text[2] + ' ' + text[1]
                            Number = text[3]
                            Explaination = text[4]

                            if patient.patient_id in Explaination or patient.patient_name in Explaination or item in Explaination:
                                if 'Modify Dicom infomation' or 'FROM StudyInformation' or 'FROM Patient' or 'Export File Path' in line:
                                    self.viewrexlogAnalyze(Time, Explaination)

    def viewrexlogAnalyze(self, Time, Explaination):
        self.viewrexlog_dataframe.loc[self.index] = [Time, 'Modify', Explaination]
        self.index += 1



                        #else:
                            #self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, None, None, Explaination]
                            #self.index += 1

        #self.viewrexlog_dataframe.index = self.viewrexlog_dataframe.index + 1
        #self.viewrexlog_dataframe['Time'] = pd.to_datetime(self.viewrexlog_dataframe['Time'])
        #self.viewrexlog_resultdf = self.viewrexlog_dataframe.groupby([pd.Grouper(key='Time', freq='D'), 'Action'])['Action'].agg(['count'])
        pd.set_option('display.max_columns', None)

        self.create_table_widget(self.viewrexlog_dataframe, widget = self.tableWidget)


    def fileview(self, fpath, treeWidget):
        fdata = [
            {"type": "Time",
             "objects": [("Creation Time", str(os.path.getctime(fpath))), ("Access Time", str(os.path.getatime(fpath))),
                         ("Modification Time", str(os.path.getmtime(fpath)))]},
            {"type": "Information",
             "objects": [("File Path", fpath), ("File Name", str(os.path.basename(fpath))),
                         ("File Size", str(os.path.getsize(fpath)) + "Byte")]},
        ]

        for d in fdata:
            parent = self.add_tree_root(d['type'], "", treeWidget)
            for child in d['objects']:
                self.add_tree_child(parent, *child)

    def create_table_widget(self, df, widget):
        widget.setRowCount(len(df.index))
        widget.setColumnCount(len(df.columns))
        widget.setHorizontalHeaderLabels(df.columns)
        widget.setVerticalHeaderLabels([str(item) for item in df.index])

        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index, col_index, item)
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

    app.exec_()
