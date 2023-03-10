import os
import datetime

# 만든시간을 타임 스탬프로 출력
def extract_metadata(path):
    ctime = timestamp(os.path.getctime(path))
    # 수정시간을 타임 스탬프로 출력
    mtime = timestamp(os.path.getmtime(path))
    # 마지막 엑세스시간을 타임 스탬프로 출력
    atime = timestamp(os.path.getatime(path))
    # 파일크기

    filesize = os.path.getsize(path)


    return ctime, mtime, atime, filesize

def timestamp(time):
    realtime = datetime.datetime.fromtimestamp(time)
    return realtime


def signature():
    #for dicom_file in dicom_files:
    try:
        hash = hash_check(dicom_file)
        real_signature = signature_check(dicom_file)
        dicom_file_info = dicom(dicom_file)
        if real_signature:
            signature_ch = "이 DICOM 파일의 시그니처는 변조되었습니다."
        else:
            signature_ch = "이 DICOM 파일의 시그니처는 변조되지 않았습니다."


    except Exception as e:
        print("더없음 : {e}")