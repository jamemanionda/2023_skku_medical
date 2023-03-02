"""
 2023.02.23 # 박재현
 수정1차 : DICOM 분석
 수정3차 : DICOM Tag 주석으로 추가
 수정4차 : UI 출력을 위한 Form 클래스 추가, DicomInformation.output_dicom_data 함수에 Form 클래스 삽입, Form UI 크기 조절 필요
 #이은지
 수정 2차 : GUI 연결(pyside import 추가,
"""
import sys

#pip install pydicom

import pydicom
import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QMainWindow, QTreeWidgetItem
from PySide6.QtGui import QAction, QIcon
from qt_material import apply_stylesheet
from mainui import Ui_MainWindow

class DicomInformation(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None, openAction=None):
        self.dicom_filepath = ''
        self.dicom_filename = ''
        self.file_meta_information_version = ''
        self.media_storage_sop_class_uid = ''
        self.media_storage_sop_instance_uid = ''
        self.patient_name = ''
        self.patient_id = ''
        self.patient_sex = ''
        self.patient_birthday = ''
        self.patient_age = ''
        self.patient_height = ''
        self.patient_weight = ''
        self.series_date = ''
        self.performing_physician_name = ''
        self.institution_name = ''
        self.institution_address = ''

        #UI 설정
        super(DicomInformation, self).__init__(parent)
        self.main = QUiLoader().load('main.ui', self)
        self.setupUi(self)
        apply_stylesheet(self, 'light_pink.xml')

        #메인 기능
        self.mainfunction()


    #파일 경로 입력
    def input_dicom(self):
        dicom_filename = QFileDialog.getOpenFileName(self, 'Open File', dir='C:')
        self.dicom_filepath = str(dicom_filename[0])
        fileobject = self.dicom_filepath.split('/')
        file = fileobject[len(fileobject) - 1]
        self.fname = file
        #self.label.setText(file)

        self.get_dicom_data()
        self.output_dicom_data()


    #dicom파일 데이터 획득
    def get_dicom_data(self):
        dcm = pydicom.dcmread(str(self.dicom_filepath))
        self.dicom_filename = os.path.basename(self.dicom_filepath)

        #파일 데이터
        self.file_meta_information_version = dcm.file_meta.get("FileMetaInformationVersion")                 #filemeta 버전
        self.media_storage_sop_class_uid = dcm.file_meta.get("MediaStorageSOPClassUID")                      #SOP class UID
        self.media_storage_sop_instance_uid = dcm.file_meta.get("MediaStorageSOPInstanceUID")                #SOP instance UID
        """
        MAC ID Number                               MAC 매개변수 시퀀스 항목 식별 번호
        MAC Algorithm                               MAC 생성에 사용되는 알고리즘
        Signature                                   암호화된 MAC
        """

        #환자 데이터
        self.patient_name = dcm.get("PatientName")                                                           #환자 이름
        self.patient_id = dcm.get("PatientID")                                                               #환자 ID
        self.patient_sex = dcm.get("PatientSex")                                                             #환자 성별
        self.patient_birthday = dcm.get("PatientBirthDate")                                                  #환자 생년월일
        self.patient_age = dcm.get("PatientAge")                                                             #환자 나이
        self.patient_height = dcm.get("PatientSize")                                                         #환자 키
        self.patient_weight = dcm.get("PatientWeight")                                                       #환자 몸무게
        self.series_date = dcm.get("SeriesDate")                                                             #진료 시작 날짜(추정)
        self.performing_physician_name = dcm.get("PerformingPhysicianName")                                  #주치의
        #이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능



        #병원 데이터
        self.institution_name = dcm.get("InstitutionName")                                                   #병원 이름
        self.institution_address = dcm.get("InstitutionAddress")                                             #병원 주소


    #dicom파일 데이터 출력
    def output_dicom_data(self):
        self.dicomTags.setText(self.dicom_filename)

        form = Form(self)
        form.show()


    def mainfunction(self):
        self.fileSelect.clicked.connect(self.input_dicom)


class Form(QWidget):
    def __init__(self, dicom):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("QTreeWidget Column")
        self.setFixedWidth(210)
        self.setFixedHeight(150)

        # 데이터
        data = [
            {"type": "File",
             "objects": [("File name", dicom.dicom_filename), ("File Meta Information Version", dicom.file_meta_information_version),
                         ("Media Storage SOP Class UID", dicom.media_storage_sop_class_uid), ("Media Storage SOP Instance UID", dicom.media_storage_sop_instance_uid)]},
            {"type": "Patient",
             "objects": [("Patient Name", dicom.patient_name), ("Patient ID", dicom.patient_id),
                         ("Patient Sex", dicom.patient_sex), ("Patient Birthday", dicom.patient_birthday),
                         ("Patient Age", dicom.patient_age), ("Patient Height", dicom.patient_height),
                         ("Patient Weight", dicom.patient_weight), ("Series Date", dicom.series_date),
                         ("Performing Physician's Name", dicom.performing_physician_name)]},
            {"type": "Institution",
             "objects": [("Institution Name", dicom.institution_name), ("Institution Address", dicom.institution_address)]},
        ]
        # QTreeView 생성 및 설정
        self.tw = QTreeWidget(self)
        self.tw.setColumnCount(2)

        for d in data:
            parent = self.add_tree_root(d['type'], "")
            for child in d['objects']:
                self.add_tree_child(parent, *child)

    def add_tree_root(self, name:str, description:str):
        item = QTreeWidgetItem(self.tw)
        item.setText(0, name)
        item.setText(1, description)
        return item

    def add_tree_child(self, parent:QTreeWidgetItem, name:str, description:str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, description)
        parent.addChild(item)
        return item

if __name__ == '__main__':
    #app = QApplication(sys.argv)
    app = QApplication(sys.argv)

    ex = DicomInformation()
    ex.show()
    app.exec()
