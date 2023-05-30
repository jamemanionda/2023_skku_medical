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


from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from qt_material import apply_stylesheet
from PyQt5 import uic
#from mainui import Ui_MainWindow
import _5_metadata
form_class = uic.loadUiType("main.ui")[0]
class single_DicomInformation(QMainWindow, form_class):

    def __init__(self):


        #UI 설정
        super().__init__()
        #super(single_DicomInformation, self).__init__(parent)

        self.setupUi(self)
        #apply_stylesheet(self, 'light_pink.xml')
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
        self.performing_physician_name=''
        self.institution_name=''
        self.institution_address=''
        #메인 기능
        self.mainfunction()



    #파일 경로 입력
    def input_dicom(self):
        dicom_filename = QFileDialog.getOpenFileName(self, 'Open File', dir='C:')
        self.dicom_filepath = str(dicom_filename[0])
        fileobject = self.dicom_filepath.split('/')
        self.dicom_filepath = "I000001_1937.dcm"
        file = fileobject[len(fileobject) - 1]
        self.fname = file
        #self.label.setText(file)
        #print(_5_metadata.extract_metadata(self.dicom_filepath))
        self.anaylze.clicked.connect(self.analyze_start)
        self.get_dicom_data()
        self.output_dicom_data()

    def analyze_start(self):
        self.get_dicom_data()
        self.output_dicom_data()

    #dicom파일 데이터 획득
    def get_dicom_data(self):
        self.dcm = pydicom.dcmread(str(self.dicom_filepath))
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
        self.tagview()

    #dicom파일 데이터 출력
    def output_dicom_data(self):
        #파일 데이터 출력

        #self.dicomTags.setText(self.dicom_filename)
        """
        print("File Name :", end=" ")
        print(self.dicom_filename)
        print("File Meta Information Version :", end=" ")
        print(self.file_meta_information_version)
        print("Media Storage SOP Class UID :", end=" ")
        print(self.media_storage_sop_class_uid)
        print("Media Storage SOP Instance UID :", end=" ")
        print(self.media_storage_sop_instance_uid)

        #환자 데이터 출력
        #DICOM 파일에 해당 attribute가 없다면 출력값이 None
        print("Patient Name :", end=" ")
        print(self.patient_name)
        print("Patient ID :", end=" ")
        print(self.patient_id)
        print("Patient Sex :", end=" ")
        print(self.patient_sex)
        print("Patient Birthday :", end=" ")
        print(self.patient_birthday)
        print("Patient Age :", end=" ")
        print(self.patient_age)
        print("Patient Height :", end=" ")
        print(self.patient_height)
        print("Patient Weight :", end=" ")
        print(self.patient_weight)
        print("Series Date :", end=" ")
        print(self.series_date)

        #print(dcm) #DICOM 파일의 모든 정보
        """
        """
        pixmap = QPixmap(self.dicom_filepath)
        scene = QGraphicsScene()
        # item = QGraphicsPixmapItem(pixmap)
        view = self.dicomView(scene)
        # scene.addItem(item)
        # self.dicomView.setScene(scene)
        view.show()
        """
    def mainfunction(self):
        self.fileSelect.clicked.connect(self.input_dicom)



    def tagview(self):
        data = [
            {"type": "File",
             "objects": [("File name", self.dicom_filename), ("File Meta Information Version", self.file_meta_information_version),
                         ("Media Storage SOP Class UID", self.media_storage_sop_class_uid), ("Media Storage SOP Instance UID", self.media_storage_sop_instance_uid)]},
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
        self.tableWidget.setColumnCount(2)
        # 0303 sy
        pixmap = QPixmap(self.dicom_filepath)
        print('1')
        scene = QGraphicsScene()
        print('2')
        item = QGraphicsPixmapItem(pixmap)
        print('3')
        scene.addItem(item)
        print('4')


        for d in data:
            parent = self.add_tree_root(d['type'], "")
            for child in d['objects']:
                self.add_tree_child(parent, *child)

        dicomImage = QImage(self.dcm.pixel_array, self.dcm.pixel_array.shape[1], self.dcm.pixel_array.shape[0],
                            QImage.Format_Grayscale8)
        self.setDicomImage(dicomImage)
        #self.display_video_in_dicom_view()


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
        scene = QGraphicsScene(self)
        scene.addPixmap(QPixmap.fromImage(image))

        self.dicomView.setScene(scene)
        #self.dicomView.fitInView(QSize(200, 200), Qt.KeepAspectRatio)




if __name__ == '__main__':
    #app = QApplication(sys.argv)
    app = QApplication(sys.argv)

    ex = single_DicomInformation()


    ex.show()

    app.exec()
