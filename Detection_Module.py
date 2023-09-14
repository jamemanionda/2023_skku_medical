import datetime
from collections import Counter

#위변조 탐지
class DetectionModule():
    #초기화
    def __init__(self):
        self.diff_vars = []




    #원본과 대조, 다른 값이 있다면 추가

    def compare_data(self, a, b, path=''):
        if isinstance(a, dict):
            for key in a:
                if key in b:
                    new_path = f"{path}.{key}" if path else key
                    self.compare_data(a[key], b[key], new_path)
                else:
                    print(f"Different key found at {path}: {key}")
                    diff = {'path': f"{path}.{key}" if path else key, 'a': a[key], 'b': None}
                    self.diff_vars.append(diff)
        elif isinstance(a, list):
            for i in range(min(len(a), len(b))):
                new_path = f"{path}[{i}]" if path else f"[{i}]"
                self.compare_data(a[i], b[i], new_path)
            if len(a) != len(b):
                print(f"Different list lengths found at {path}: {len(a)} != {len(b)}")
        else:
            if a != b:
                if a[0] == 'File name':
                    pass
                print(f"Different value found at {path}: {a} != {b}")
                a_key = a[0] if isinstance(a, tuple) else None
                #diff = {'path': path, 'a': a, 'b': b}
                diff = a_key
                self.diff_vars.append(diff)

        # if self.extract_DA(a):
        #     diff = 'a에서'+self.extract_DA(a)
        #
        #     self.diff_vars.append(diff)
        # if self.extract_DA(b):
        #     diff = 'b에서' + self.extract_DA(b)
        #
        #     self.diff_vars.append(diff)

        return self.diff_vars







#테스트
