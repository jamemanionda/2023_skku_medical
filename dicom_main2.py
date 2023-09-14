"""
 2023.02.23 # 박재현
 수정1차 : DICOM 분석
 수정3차 : DICOM Tag 주석으로 추가
 수정4차 : UI 출력을 위한 Form 클래스 추가, DicomInformation.output_dicom_data 함수에 Form 클래스 삽입, Form UI 크기 조절 필요
 #이은지
 수정 2차 : GUI 연결(pyside import 추가,
"""
import datetime
import glob
import sys
import datetime
from collections import Counter

#import dicom as dicom
import pandas as pd
#pip install pydicom

import pydicom
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QGraphicsScene, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant, QSize
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import dicomANDpacs
import report2
from Detection_Module import DetectionModule


form_class = uic.loadUiType("dicom2.ui")[0]
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
        self.study_date = str(dcm.get("StudyDate"))  # 진료 시작 날짜(추정)
        self.series_date = str(dcm.get("SeriesDate"))  # 진료 시작 날짜(추정)
        self.acquisition_date = str(dcm.get("AcquisitionDate"))
        self.content_date = str(dcm.get("ContentDate"))
        # 이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능
        self.performing_physician_name = str(dcm.get("PerformingPhysicianName"))  # 주치의
class DicomInformation(QMainWindow, form_class):

    def __init__(self):
        self.filepath_list = []

        #UI 설정
        super().__init__() #super(DicomInformation, self).__init__(parent)
        self.setupUi(self)

        self.addressip = '192.168.0.1'
        # self.fname = 'hello'
        # 메인 기능
        # self.mainfunction()
        self.reportbtn.clicked.connect(lambda: self.makeReport())


        self.fileSelect.clicked.connect(self.input_dicom_file1)
        self.fileSelect2.clicked.connect(self.input_dicom_file2)
        self.analyze_btn.clicked.connect(self.compare)

        self.OK_btn.clicked.connect(self.accept)
        self.Cancel_btn.clicked.connect(self.reject)

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
            self.realpath = report2.make_docx(self.addressip, self.file1, self.file2, self.diffs)
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

    def extract_DA(self, a):
        values = []

        strr = ['Study Date', 'Series Date', 'Content Date']
        for i in strr :
            result = [tup[1] for tup in a if tup[0] == i][0]
            values.append(result)
        return values

    def detection_DA(self, values):

        date1, date2, date3 = values
        counter = Counter([date1, date2, date3])

        if counter.most_common(1)[0][1] == 3:
            print("이 파일의 date 값은 이상없습니다.")
        else:
            most_common_values = counter.most_common(2)
            common_value, count = most_common_values[0]
            changed_value, _ = most_common_values[1]
            print(f"원본파일의 날짜는 {common_value} 값으로 예상됩니다.")
            print(f"{changed_value} 값으로 변경된 것으로 예상됩니다.")

            return common_value, changed_value



    def compare(self):
        data1, dcm1, patient1 = self.get_dicom_data(self.dicom_filepath)
        data2, dcm2, patient2 = self.get_dicom_data(self.dicom_filepath2) #0322
        c = DetectionModule()
        self.file_Forgery_Position_text.setText('')
        self.diffs = c.compare_data(data1, data2)

        values = self.extract_DA(data1[1]['objects'])
        a = self.detection_DA(values)
        if a is not None:

            diff = 'a에서' + a

            self.diff_vars.append(diff)

        values = self.extract_DA(data2[1]['objects'])

        if self.detection_DA(values):
            diff = 'a에서' + self.detection_DA(values)

            self.diff_vars.append(diff)


        if len(self.diffs) == 0:
            self.file_isForgery_text.setText('위변조 의심 행위가 없습니다')
        else:
            self.file_isForgery_text.setText('위변조 의심 행위가 있습니다')
            self.file_Forgery_Position_text.setText(str(self.diffs))

        self.TagInfo1_Widget.clear()
        self.TagInfo2_Widget.clear()
        self.FileInfo1_Widget.clear()
        self.FileInfo2_Widget.clear()

        image1 = self.tagview2(data1, self.TagInfo1_Widget, dcm1)
        image2 = self.tagview2(data2, self.TagInfo2_Widget, dcm2)

        #하위 4줄 #제거
        scene = self.setDicomImage(image1)
        scene2 = self.setDicomImage(image2)
        self.screen1_Widget.setScene(scene)
        self.screen2_Widget.setScene(scene2)

        self.fileview(self.dicom_filepath, self.FileInfo1_Widget)
        self.fileview(self.dicom_filepath2, self.FileInfo2_Widget)
        # self.screen1_Widget.fitInView(QSize(200, 200), Qt.KeepAspectRatio)
        # self.screen2_Widget.fitInView(QSize(200, 200), Qt.KeepAspectRatio)

        self.file1 = str(os.path.basename(self.dicom_filepath))
        self.file2 = str(os.path.basename(self.dicom_filepath2))
        self.dicomExtract(self.file1, patient1, self.tableWidget_1)
        self.dicomExtract(self.file2, patient2, self.tableWidget_2)

    def dicomExtract(self, item, patient, tablewidget):
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
                                if 'Modify Dicom infomation' in line:
                                    self.viewrexlog_dataframe.loc[self.index] = [Time, 'Modify', Explaination]
                                    self.index += 1

                                elif 'FROM StudyInformation' in line:
                                    self.viewrexlog_dataframe.loc[self.index] = [Time, 'Select', Explaination]
                                    self.index += 1

                                elif 'FROM Patient' in line:
                                    self.viewrexlog_dataframe.loc[self.index] = [Time, 'Select', Explaination]
                                    self.index += 1

                                elif 'Export File Path' in line:
                                    self.viewrexlog_dataframe.loc[self.index] = [Time, 'Export', Explaination]
                                    self.index += 1



                        #else:
                            #self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, None, None, Explaination]
                            #self.index += 1

        #self.viewrexlog_dataframe.index = self.viewrexlog_dataframe.index + 1
        #self.viewrexlog_dataframe['Time'] = pd.to_datetime(self.viewrexlog_dataframe['Time'])
        #self.viewrexlog_resultdf = self.viewrexlog_dataframe.groupby([pd.Grouper(key='Time', freq='D'), 'Action'])['Action'].agg(['count'])
        pd.set_option('display.max_columns', None)

        self.create_table_widget(self.viewrexlog_dataframe, widget = tablewidget)

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
                         ("Patient Weight", patient.patient_weight), ("Series Date", patient.series_date),("Study Date", patient.study_date),("Acquisition Date", patient.acquisition_date), ("Content Date", patient.content_date),
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
        #하위 4줄 #제거
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
