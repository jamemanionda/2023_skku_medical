"""
 2023.02.23 # 박재현
 수정1차 : DICOM 분석
 수정3차 : DICOM Tag 주석으로 추가
 수정4차 : UI 출력을 위한 Form 클래스 추가, DicomInformation.output_dicom_data 함수에 Form 클래스 삽입, Form UI 크기 조절 필요
 #이은지
 수정 2차 : GUI 연결(pyside import 추가,
"""
import datetime
import sys

import dicom as dicom
#pip install pydicom

import pydicom
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QGraphicsScene, QFileDialog
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant, QSize
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import dicomANDpacs
from Detection_Module import DetectionModule


form_class = uic.loadUiType("dicom.ui")[0]
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
class DicomInformation(QMainWindow, form_class):

    def __init__(self):
        self.filepath_list = []

        #UI 설정
        super().__init__() #super(DicomInformation, self).__init__(parent)
        self.setupUi(self)

        self.fileSelect.clicked.connect(self.input_dicom_file1)
        self.fileSelect2.clicked.connect(self.input_dicom_file2)
        self.analyze_btn.clicked.connect(self.compare)

        self.OK_btn.clicked.connect(self.accept)
        self.Cancel_btn.clicked.connect(self.reject)

    #파일 경로 입력
    def input_dicom_file1(self):
        dicom_filename = QFileDialog.getOpenFileName(self, 'File Load', '',
                                                     'Dicom File(*.dcm);; All File(*)')
        dcmfile = dicom_filename[0]
        self.dicom_filepath = dcmfile.replace('/', '\\')
        self.fileInput1.setText(self.dicom_filepath)
        if self.dicom_filepath not in self.filepath_list:
            self.filepath_list.append(self.dicom_filepath)

    def input_dicom_file2(self):
        dicom_filename = QFileDialog.getOpenFileName(self, 'File Load', '',
                                                         'Dicom File(*.dcm);; All File(*)')
        dcmfile = dicom_filename[0]
        self.dicom_filepath2 = dcmfile.replace('/', '\\')
        self.fileInput2.setText(self.dicom_filepath2)
        if self.dicom_filepath2 not in self.filepath_list:
            self.filepath_list.append(self.dicom_filepath2)
        #self.label.setText(file)
        #print(_5_metadata.extract_metadata(self.dicom_filepath))

    def compare(self):
        data1, dcm1 = self.get_dicom_data(self.dicom_filepath)
        data2, dcm2 = self.get_dicom_data(self.dicom_filepath2) #0322
        c = DetectionModule()
        self.file_Forgery_Position_text.setText('')

        diffs = c.compare_data(data1, data2)
        #object_values = [item["key"] for item in diffs]

        if len(diffs) == 0:
            self.file_isForgery_text.setText('위변조 의심 행위가 없습니다')
        else:
            self.file_isForgery_text.setText('위변조 의심 행위가 있습니다')
            self.file_Forgery_Position_text.setText(str(diffs))

        self.TagInfo1_Widget.clear()
        self.TagInfo2_Widget.clear()
        self.FileInfo1_Widget.clear()
        self.FileInfo2_Widget.clear()

        image1 = self.tagview2(data1, self.TagInfo1_Widget, dcm1)
        image2 = self.tagview2(data2, self.TagInfo2_Widget, dcm2)

        scene = self.setDicomImage(image1)
        scene2 = self.setDicomImage(image2)

        self.screen1_Widget.setScene(scene)
        self.screen2_Widget.setScene(scene2)

        self.fileview(self.dicom_filepath, self.FileInfo1_Widget)
        self.fileview(self.dicom_filepath2, self.FileInfo2_Widget)
        #self.screen1_Widget.fitInView(QSize(200, 200), Qt.KeepAspectRatio)
        #self.screen2_Widget.fitInView(QSize(200, 200), Qt.KeepAspectRatio)

    #dicom파일 데이터 획득
    def get_dicom_data(self, file):
        dcm = pydicom.dcmread(str(file))
        dicom_filename = os.path.basename(file)

        # 파일 데이터


        # 환자 데이터
        patient1 = Patient_1(dcm)

        # 병원 데이터
        institution1 = Institution_1(dcm)

        data = self.tagview(file, patient1, institution1)
        return data, dcm







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
        dicomImage = QImage(dcm.pixel_array, dcm.pixel_array.shape[1], dcm.pixel_array.shape[0],
                            QImage.Format_Grayscale8)

        #self.display_video_in_dicom_view()
        return dicomImage


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
    def setDicomImage(self, image):
        scene = QGraphicsScene(self)
        from PyQt5.QtGui import QPixmap
        scene.addPixmap(QPixmap.fromImage(image))

        return scene

    def fileview(self, fpath, treeWidget):
        ctime = datetime.datetime.fromtimestamp(os.path.getctime(fpath))
        atime = datetime.datetime.fromtimestamp(os.path.getatime(fpath))
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
        fdata = [
            {"type": "Time",
             "objects": [("Creation Time", str(ctime)), ("Access Time", str(atime)),
                         ("Modification Time", str(mtime))]},
            {"type": "Information",
             "objects": [("File Path", fpath), ("File Name", str(os.path.basename(fpath))),
                         ("File Size", str(os.path.getsize(fpath)) + "Byte")]},
        ]

        for d in fdata:
            parent = self.add_tree_root(d['type'], "", treeWidget)
            for child in d['objects']:
                self.add_tree_child(parent, *child)

    def accept(self):
        self.dnp = dicomANDpacs.dicomandpacsmain()
        self.dnp.update_dcmlist(self.filepath_list)
        self.dnp.show()
        #self.dnp.dicom_filepath = self.filepath_list
        self.close()

    def reject(self):
        self.close()


if __name__ == '__main__':
    #app = QApplication(sys.argv)
    app = QApplication(sys.argv)

    ex = DicomInformation()


    ex.show()

    app.exec_()
