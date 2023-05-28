import datetime
from collections import Counter


def extract_DA(filepath):
    with open(filepath, "rb") as f:
        data = f.read(400)

    # DATE 시그니처의 위치 찾기
    start_index = data.find(b"\x44\x41\x08\x00")

    # 시그니처 이후 16바이트씩 3개의 값을 추출

    values = []
    for i in range(3):
        if i == 0:
            offset = start_index
        else :
            offset = start_index + i*16
        value = data[offset+4:offset+12]
        values.append(value)

    return values

def detection_DA(values):

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




filepath = input(filepath)
values = extract_DA(filepath)
detection_DA(values)