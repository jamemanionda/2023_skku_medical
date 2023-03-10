import pydicom
import os
import sys
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class Dicom_Information:
    def __init__(self):
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
        self.input_dicom()


    #파일 경로 입력
    def input_dicom(self):
        #self.dicom_filepath = input("파일 경로 :")
        self.dicom_filepath = "D:\Download\I000001_1937.dcm"
        self.get_dicom_data()
        self.output_dicom_data()


    #dicom파일 데이터 획득
    def get_dicom_data(self):
        dcm = pydicom.dcmread(str(self.dicom_filepath))
        self.dicom_filename = os.path.basename(self.dicom_filepath)

        #파일 데이터
        self.file_meta_information_version = str(dcm.file_meta.get("FileMetaInformationVersion"))                   #filemeta 버전
        self.media_storage_sop_class_uid = str(dcm.file_meta.get("MediaStorageSOPClassUID"))                        #SOP class UID
        self.media_storage_sop_instance_uid = str(dcm.file_meta.get("MediaStorageSOPInstanceUID"))                  #SOP instance UID

        #환자 데이터
        self.patient_name = str(dcm.get("PatientName"))                                                             #환자 이름
        self.patient_id = str(dcm.get("PatientID"))                                                                 #환자 ID
        self.patient_sex = str(dcm.get("PatientSex"))                                                               #환자 성별
        self.patient_birthday = str(dcm.get("PatientBirthDate"))                                                    #환자 생년월일
        self.patient_age = str(dcm.get("PatientAge"))                                                               #환자 나이
        self.patient_height = str(dcm.get("PatientSize"))                                                           #환자 키
        self.patient_weight = str(dcm.get("PatientWeight"))                                                         #환자 몸무게
        self.series_date = str(dcm.get("SeriesDate"))                                                               #진료 시작 날짜(추정)
        #이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능
        self.performing_physician_name = str(dcm.get("PerformingPhysicianName"))                                    #주치의

        # 병원 데이터
        self.institution_name = str(dcm.get("InstitutionName"))                                                     #병원 이름
        self.institution_address = str(dcm.get("InstitutionAddress"))                                               #병원 주소


        #dicom 데이터 출력
    def output_dicom_data(self):
        """
        #파일 데이터 출력
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
        """

        app = QApplication(sys.argv)
        form = Form(self)
        form.show()
        exit(app.exec_())

class Form(QWidget):
    def __init__(self, dicom):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("DICOM Information")
        #self.scaled(400,400)
        #self.setFixedWidth(300)
        #self.setFixedHeight(150)


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
             "objects": [("Institution Name", dicom.institution_name),
                         ("Institution Address", dicom.institution_address)]},
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

a = Dicom_Information()
a