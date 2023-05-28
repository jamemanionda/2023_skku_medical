import os

import pydicom



def input_dicom():

    dicom_filepath = "forgedviewer.dcm"

    data1 = get_dicom_data(dicom_filepath)

def get_dicom_data(file):
    dcm = pydicom.dcmread(str(file))
    dicom_filename = os.path.basename(file)

    # 파일 데이터

    # 환자 데이터
    patient1 = Patient_1(dcm)


class Patient_1():
    def __init__(self, dcm):
        self.patient_name = str(dcm.get("PatientName"))  # 환자 이름
        self.study_date = str(dcm.get("StudyDate"))
        isForgeSuspicion = 0

        if "Generated with" and "Viewer" in self.patient_name :
            isForgeSuspicion += 1
        if self.study_date == '':
            isForgeSuspicion += 1

        if isForgeSuspicion >= 2:
            print("Microdicom 주석 조작이 의심됩니다")
        else :
            print("의심되는 행위가 없습니다.")


input_dicom()
