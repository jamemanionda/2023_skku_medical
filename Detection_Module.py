class DetectionModule():
    def __init__(self):
        self.diff_vars = []

    def compare(self, a, b):
        for key, value in a.__dict__.items():
            if value != b.__dict__[key]:
                self.diff_vars.append(key)
        self.detection()

    def detection(self):
        if len(self.diff_vars) == 0:
            print("위조되지 않음")
        else:
            print("위조됨")
            print("위조 추정 위치 : ", self.diff_vars)