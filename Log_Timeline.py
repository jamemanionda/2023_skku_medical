import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#로그 시각화
class LogTimeline:
    #초기화
    def __init__(self):
        self.logfile_path = ''
        self.logdf = pd.DataFrame()
        self.visualdf = pd.DataFrame()

    #로그 파일 불러오기
    def input_logfile(self):
        #self.logfile_path = input("logfile path: ")
        self.logfile_path = 'PACSSERVER-20230315-0743.log'
        self.logdf = pd.read_table(self.logfile_path, sep='\t', encoding='UTF-16')
        self.logdf['Timestamp'] = pd.to_datetime(self.logdf['Timestamp'])

    #로그 파일 시각화
    def visualization(self):
        tmpdf = self.logdf.loc[self.logdf['EventID'] != 'bjtco']        #EventID를 임의로 파일에 가한 행위 기록이라고 가정
        self.visualdf = tmpdf[['Timestamp', 'EventID']]                 #timestamp와 행위기록만 추출

        self.visualdf = self.visualdf.set_index('Timestamp')
        self.visualdf = self.visualdf.resample('5L').count()            #5ms 단위로 timestamp를 그룹화, 해당 값에 대해 변경 필요

        self.visualdf.plot(kind='bar')                                  #바 형태의 그래프로 시각화
        plt.xlabel("Timestamp")
        plt.ylabel("Frequency")
        plt.show()

#테스트
test = LogTimeline()
test.input_logfile()
test.visualization()