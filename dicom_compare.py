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
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, \
    QMainWindow, QTreeWidgetItem, QGraphicsPixmapItem, QGraphicsScene
from PySide6.QtGui import QAction, QIcon, QPixmap, QImage
from qt_material import apply_stylesheet
from compare_ui import Ui_MainWindow
import _5_metadata
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
class DicomInformation(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None, openAction=None):
        dicom_filepath = ''
        dicom_filename = ''
        file_meta_information_version = ''
        media_storage_sop_class_uid = ''
        media_storage_sop_instance_uid = ''
        patient_name = ''
        patient_id = ''
        patient_sex = ''
        patient_birthday = ''
        patient_age = ''
        patient_height = ''
        patient_weight = ''
        series_date = ''
        performing_physician_name=''
        institution_name=''
        institution_address=''


        #UI 설정
        super(DicomInformation, self).__init__(parent)
        self.main = QUiLoader().load('dicom.ui', self)
        self.setupUi(self)
        apply_stylesheet(self, 'light_pink.xml')

        #메인 기능
        self.mainfunction()



    #파일 경로 입력
    def input_dicom(self):
        #dicom_filename = QFileDialog.getOpenFileName(self, 'Open File', dir='C:')
        #self.dicom_filepath = str(dicom_filename[0])
        #fileobject = self.dicom_filepath.split('/')
        self.dicom_filepath = "I000001_1937.dcm"
        self.dicom_filepath2 = "VR00001.dcm"
        #file = fileobject[len(fileobject) - 1]
        #self.fname = file
        #self.label.setText(file)
        #print(_5_metadata.extract_metadata(self.dicom_filepath))
        data1 = self.get_dicom_data(self.dicom_filepath)
        data2 = self.get_dicom_data(self.dicom_filepath2) #0322
        self.tagview2(data1, self.treeWidget)
        self.tagview2(data2, self.treeWidget_2)


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

        return data





    def mainfunction(self):
        self.fileSelect.clicked.connect(self.input_dicom)



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
        # QTreeView 생성 및 설정
        self.tableWidget.setColumnCount(2)
        self.tableWidget_2.setColumnCount(2)

        # 0303 sy
        #pixmap = QPixmap(self.dicom_filepath)
        #print('1')
        #scene = QGraphicsScene()
        #print('2')
        #item = QGraphicsPixmapItem(pixmap)
        #print('3')
        #scene.addItem(item)
        #print('4')
        return  data

    def tagview2(self, data, treeWidget):  # 0322
        for d in data:
            parent = self.add_tree_root(d['type'], "", treeWidget)
            parent2 = self.add_tree_root(d['type'], "", treeWidget)
            for child in d['objects']:
                self.add_tree_child(parent, *child)


        dicomImage = QImage(self.dcm.pixel_array, self.dcm.pixel_array.shape[1], self.dcm.pixel_array.shape[0],
                            QImage.Format_Grayscale8)
        self.setDicomImage(dicomImage)
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
    def setDicomImage(self, image):
        scene = QGraphicsScene(self)
        scene.addPixmap(QPixmap.fromImage(image))

        self.dicomView.setScene(scene)
        from PySide6.QtCore import QSize
        self.dicomView.fitInView(QSize(200, 200), Qt.KeepAspectRatio)




if __name__ == '__main__':
    #app = QApplication(sys.argv)
    app = QApplication(sys.argv)

    ex = DicomInformation()


    ex.show()

    app.exec()
