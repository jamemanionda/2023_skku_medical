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
# pip install pydicom

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
    QMainWindow, QTreeWidgetItem, QGraphicsPixmapItem, QGraphicsScene, QPushButton
from PySide6.QtGui import QAction, QIcon, QPixmap, QImage
from qt_material import apply_stylesheet
from dicom_main import DicomInformation
from compare_ui import Ui_MainWindow
from PySide6.QtCore import QSize


import _5_metadata


class MainClass(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.dicom_filepath = "I000001_1937.dcm"
        self.dicom_filepath2 = "VR00001.dcm"
        # UI 설정
        #super(MainClass, self).__init__(parent)
        self.main = QUiLoader().load('compare.ui', self)
        self.setupUi(self)
        apply_stylesheet(self, 'light_red.xml')

        dicomfile1 = DicomInformation2(self.dicom_filepath)
        dicomfile2 = DicomInformation2(self.dicom_filepath2)

        dicom_view = dicomfile1.tagview()
        dicom_view2 = dicomfile2.tagview()

        View(dicom_view, self.dicom_filepath, self.treeWidget, self.dicomView, dicomfile1.dcm)
        View(dicom_view2, self.dicom_filepath2, self.treeWidget_2, self.dicomView_2, dicomfile1.dcm)


class DicomInformation2(QMainWindow, Ui_MainWindow):

    def __init__(self, filepath, parent=None, openAction=None):
        super().__init__(parent)
        # UI 설정
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dcm = None
        self.filepath = filepath
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
        self.dcm = pydicom.dcmread(str(self.filepath))

        # 메인 기능
        self.mainfunction()



    # 파일 경로 입력


    def mainfunction(self):
        self.ui.fileSelect.clicked.connect(DicomInformation2_data(self.filepath).input_dicom)
        self.tagview()

    def tagview(self):
        data = [
            {"type": "File",
             "objects": [("File name", self.dicom_filename),
                         ("File Meta Information Version", self.file_meta_information_version),
                         ("Media Storage SOP Class UID", self.media_storage_sop_class_uid),
                         ("Media Storage SOP Instance UID", self.media_storage_sop_instance_uid)]},
            {"type": "Patient",
             "objects": [("Patient Name", self.patient_name), ("Patient ID", self.patient_id),
                         ("Patient Sex", self.patient_sex), ("Patient Birthday", self.patient_birthday),
                         ("Patient Age", self.patient_age), ("Patient Height", self.patient_height),
                         ("Patient Weight", self.patient_weight), ("Series Date", self.series_date),
                         ("Performing Physician's Name", self.performing_physician_name)]},
            {"type": "Institution",
             "objects": [("Institution Name", self.institution_name),
                         ("Institution Address", self.institution_address)]},
        ]
        # QTreeView 생성 및 설정
        self.ui.treeWidget.setColumnCount(2)
        self.ui.treeWidget_2.setColumnCount(2)
        # 0303 sy

        return data



class View():
    def __init__(self, data, filepath, treewidget, dicomView, dcm, parent=None, openAction=None):
        self.treeWidget = treewidget
        self.dicomView = dicomView
        self.dcm = dcm
        for d in data:
            parent = self.add_tree_root(d['type'], "")
            for child in d['objects']:
                self.add_tree_child(parent, *child)

        dicomImage = QImage(self.dcm.pixel_array, self.dcm.pixel_array.shape[1], self.dcm.pixel_array.shape[0],
                            QImage.Format_Grayscale8)
        self.setDicomImage(dicomImage)

        # self.display_video_in_dicom_view()

    def add_tree_root(self, name: str, description: str):
        item = QTreeWidgetItem(self.treeWidget)
        item.setText(0, name)
        item.setText(1, description)
        return item

    def add_tree_child(self, parent: QTreeWidgetItem, name: str, description: str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, description)
        parent.addChild(item)
        return item

    def setDicomImage(self, image):
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(image))

        self.dicomView.setScene(scene)

        #self.dicomView.fitInView(QSize(200, 200), Qt.KeepAspectRatio)


class DicomInformation2_data():
    def __init__(self, parent=None, openAction=None):
        self.dicom_filepath = None
        self.dicom_filepath2 = None
        self.dcm = None

    def input_dicom(self):
        #dicom_filename = QFileDialog.getOpenFileName(self, 'Open File', dir='C:')
        #self.dicom_filepath = str(dicom_filename[0])
        #fileobject = self.dicom_filepath.split('/')
        #fileobject2 = self.dicom_filepath.split('/')

        #file = fileobject[len(fileobject) - 1]
        #self.fname = file
        # self.label.setText(file)
        #print(_5_metadata.extract_metadata(self.dicom_filepath))
        self.get_dicom_data()

    # dicom파일 데이터 획득
    def get_dicom_data(self):
        #self.dcm = pydicom.dcmread(str(self.dicom_filepath)) #0323
        self.dicom_filename = os.path.basename(self.dicom_filepath)

        # 파일 데이터
        self.file_meta_information_version = str(self.dcm.file_meta.get("FileMetaInformationVersion"))  # filemeta 버전
        self.media_storage_sop_class_uid = str(self.dcm.file_meta.get("MediaStorageSOPClassUID"))  # SOP class UID
        self.media_storage_sop_instance_uid = str(self.dcm.file_meta.get("MediaStorageSOPInstanceUID"))  # SOP instance UID

        # 환자 데이터
        self.patient_name = str(self.dcm.get("PatientName"))  # 환자 이름
        self.patient_id = str(self.dcm.get("PatientID"))  # 환자 ID
        self.patient_sex = str(self.dcm.get("PatientSex"))  # 환자 성별
        self.patient_birthday = str(self.dcm.get("PatientBirthDate"))  # 환자 생년월일
        self.patient_age = str(self.dcm.get("PatientAge"))  # 환자 나이
        self.patient_height = str(self.dcm.get("PatientSize"))  # 환자 키
        self.patient_weight = str(self.dcm.get("PatientWeight"))  # 환자 몸무게
        self.series_date = str(self.dcm.get("SeriesDate"))  # 진료 시작 날짜(추정)
        # 이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능
        self.performing_physician_name = str(self.dcm.get("PerformingPhysicianName"))  # 주치의

        # 병원 데이터
        self.institution_name = str(self.dcm.get("InstitutionName"))  # 병원 이름
        self.institution_address = str(self.dcm.get("InstitutionAddress"))  # 병원 주소

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    app = QApplication(sys.argv)

    a = MainClass()

    a.show()

    app.exec()
