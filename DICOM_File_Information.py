import pydicom
import os
DICOM_Filepath = ''                         #파일 경로 입력
dcm = pydicom.dcmread(DICOM_Filepath)

DICOM_Filename = os.path.basename(DICOM_Filepath)   #파일명 추출

patient_Name = dcm.PatientName                      #환자 이름
patient_ID = dcm.PatientID                          #환자 ID
patient_Sex = dcm.PatientSex                        #환자 성별
patient_Birthday = dcm.PatientBirthDate             #환자 생년월일
study_Date = dcm.StudyDate                          #진료 시작 날짜(추정)

print("File Name :", end=" ")
print(DICOM_Filename)
print("Patient Name :", end=" ")
print(patient_Name)
print("Patient ID :", end=" ")
print(patient_ID)
print("Patient Sex :", end=" ")
print(patient_Sex)
print("Patient Birthday :", end=" ")
print(patient_Birthday)
print("Study Date :", end=" ")
print(study_Date)

#print(dcm) DICOM 파일의 모든 정보


