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