import struct
import os.path
import time

def extract_dicom_signature(filepath):
    # 파일의 MAC 타임 정보 추출
    mtime = os.path.getmtime(filepath) # 수정 시간 (Modification time)
    atime = os.path.getatime(filepath) # 접근 시간 (Access time)
    ctime = os.path.getctime(filepath) # 생성 시간 (Creation time)



def extract_dicom_signature(filename):
    with open(filename, 'rb') as f:
        # DICOM signature is located at byte offset 128
        f.seek(128)
        signature = f.read(4)
        # Convert the signature to string format
        signature_str = struct.unpack('4s', signature)[0].decode('utf-8')
        if signature_str == 'DICM':
            return True
        else:
            return False




#extract_dicom_signature("I000001_1937.dcm")
