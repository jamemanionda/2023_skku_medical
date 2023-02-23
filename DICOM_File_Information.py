#pip install pydicom

import pydicom
import os

DICOM_Filepath = ''                         #파일 경로 입력
dcm = pydicom.dcmread(str(DICOM_Filepath))

DICOM_Filename = os.path.basename(DICOM_Filepath)                                               #파일명 추출

#파일 정보
file_Meta_Information_Version = dcm.file_meta.get("FileMetaInformationVersion")                 #filemeta 버전
media_Storage_SOP_Class_UID = dcm.file_meta.get("MediaStorageSOPClassUID")                      #SOP class UID
media_Storage_SOP_Instance_UID = dcm.file_meta.get("MediaStorageSOPInstanceUID")                #SOP instance UID

#환자 정보
patient_Name = dcm.get("PatientName")                                                           #환자 이름
patient_ID = dcm.get("PatientID")                                                               #환자 ID
patient_Sex = dcm.get("PatientSex")                                                             #환자 성별
patient_Birthday = dcm.get("PatientBirthDate")                                                  #환자 생년월일
patient_Age = dcm.get("PatientAge")                                                             #환자 나이
patient_Height = dcm.get("PatientSize")                                                         #환자 키
patient_Weight = dcm.get("PatientWeight")                                                       #환자 몸무게
study_Date = dcm.get("StudyDate")                                                               #진료 시작 날짜(추정)
#이 외의 알레르기, 흡연, 임신 등 기타 상태 확인 가능

#파일 정보 출력
print("File Name :", end=" ")
print(DICOM_Filename)
print("File Meta Information Version :", end=" ")
print(file_Meta_Information_Version)
print("Media Storage SOP Class UID :", end=" ")
print(media_Storage_SOP_Class_UID)
print("Media Storage SOP Instance UID :", end=" ")
print(media_Storage_SOP_Instance_UID)

#환자 정보 출력
#DICOM 파일에 해당 attribute가 없다면 출력값이 None
print("Patient Name :", end=" ")
print(patient_Name)
print("Patient ID :", end=" ")
print(patient_ID)
print("Patient Sex :", end=" ")
print(patient_Sex)
print("Patient Birthday :", end=" ")
print(patient_Birthday)
print("Patient Age :", end=" ")
print(patient_Age)
print("Patient Height :", end=" ")
print(patient_Height)
print("Patient Weight :", end=" ")
print(patient_Weight)
print("Study Date :", end=" ")
print(study_Date)

#print(dcm) #DICOM 파일의 모든 정보


