
"""
 2023.02.22 # 이서연
 수정1차 : 해시값 확인
 수정2차 : 시그니처 위변조 확인
 수정3차 : 파일이름, 환자이름, 환자ID, 날짜정보, 시간정보 등을 CSV 파일로 시간순으로 추출
 수정4차 : 한 DICOM 파일이 아닌 여러개의 DICOM 파일을 받아서 검사핤 수 있게
"""
        for dicom_file in dicom_files:
            try:
                hash = hash_check(dicom_file)
                real_signature = signature_check(dicom_file)
                dicom_file_info = dicom(dicom_file)
                if real_signature:
                    signature_ch = "이 DICOM 파일의 시그니처는 변조되었습니다."
                else:
                    signature_ch = "이 DICOM 파일의 시그니처는 변조되지 않았습니다."

                writer.writerow({'File Name': dicom_file_info[0],
                                 'Hash': hash,
                                 'Signature': signature_ch,
                                 'Patient Name': dicom_file_info[1],
                                 'Patient ID': dicom_file_info[2],
                                 'Modality': dicom_file_info[3],
                                 'Creation Time': dicom_file_info[4],
                                 'Modification Time': dicom_file_info[5],
                                 'Access Time': dicom_file_info[6]})
            except Exception as e:
                print("더없음 : {e}")

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_rows = sorted(reader, key=lambda row: row['Modification Time'])

    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Hash', 'Signature', 'Patient Name', 'Patient ID', 'Modality','Creation Time','Access Time','Modification Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)

def dicomcsv(csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_rows = sorted(reader, key=lambda row: row['Modification Time'])
        for row in sorted_rows:
            print("{'File Name':}:           {row['File Name']}")
            print("{'Hash':}:                {row['Hash']}")
            print("{'Signature':}:           {row['Signature']}")
            print("{'Patient Name':}:        {row['Patient Name']}")
            print("{'Patient ID':}:          {row['Patient ID']}")
            print("{'Modality':}:            {row['Modality']}")
            print("{'Modification Time':}:   {row['Modification Time']}\n")
            print("{'Access Time':}:         {row['Access Time']}\n")
            print("{'Creation Time':}:       {row['Creation Time']}")

if __name__ == '__main__':
    dicom_files = ['test1.dcm', 'test2.dcm', 'test3.dcm']
    dicom_verification(dicom_files)
    dicomcsv('dicom.csv')