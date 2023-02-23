#pip install pydicom

import pydicom
import os

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
        self.study_date = ''

    #파일 경로 입력
    def input_dicom(self):
        self.dicom_filepath = input("파일 경로 :")

    #dicom파일 데이터 획득
    def get_dicom_data(self):
        dcm = pydicom.dcmread(str(self.dicom_filepath))
        self.dicom_filename = os.path.basename(self.dicom_filepath)

        #파일 데이터
        self.file_meta_information_version = dcm.file_meta.get("FileMetaInformationVersion")                 #filemeta 버전
        self.media_storage_sop_class_uid = dcm.file_meta.get("MediaStorageSOPClassUID")                      #SOP class UID
        self.media_storage_sop_instance_uid = dcm.file_meta.get("MediaStorageSOPInstanceUID")                #SOP instance UID

        #환자 데이터
        self.patient_name = dcm.get("PatientName")                                                           #환자 이름
        self.patient_id = dcm.get("PatientID")                                                               #환자 ID
        self.patient_sex = dcm.get("PatientSex")                                                             #환자 성별
        self.patient_birthday = dcm.get("PatientBirthDate")                                                  #환자 생년월일
        self.patient_age = dcm.get("PatientAge")                                                             #환자 나이
        self.patient_height = dcm.get("PatientSize")                                                         #환자 키
        self.patient_weight = dcm.get("PatientWeight")                                                       #환자 몸무게
        self.study_date = dcm.get("StudyDate")                                                               #진료 시작 날짜(추정)
        #이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능

    #dicom파일 데이터 출력
    def output_dicom_data(self):
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
        print("Study Date :", end=" ")
        print(self.study_date)




