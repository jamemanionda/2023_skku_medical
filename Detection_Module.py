import UI_test
a = UI_test.Dicom_Information()
b = UI_test.Dicom_Information()

#위변조 탐지
class DetectionModule():
    #초기화
    def __init__(self):
        self.diff_vars = []

    #원본과 대조, 다른 값이 있다면 딕셔너리에 추가
    def compare(self, a, b):
        for key, value in a.__dict__.items():
            if value != b.__dict__[key]:
                self.diff_vars.append(key)
        self.detection()

    #위변조 여부 판별
    def detection(self):
        if len(self.diff_vars) == 0:
            print("위조되지 않음")
        else:
            print("위조됨")
            print("위조 추정 위치 : ", self.diff_vars)

#테스트
c = DetectionModule()
c.compare(a, b)