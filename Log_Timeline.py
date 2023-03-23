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
    """
    #PACSSERVER logfile
    #로그 파일 불러오기
    def input_logfile(self):
        #self.logfile_path = input("logfile path: ")
        self.logfile_path = 'PACSSERVER-20230315-0743.log'      #로그 파일 경로 입력
        self.logdf = pd.read_table(self.logfile_path, sep='\t', encoding='UTF-16')      #DataFrame 생성
        self.logdf['Timestamp'] = pd.to_datetime(self.logdf['Timestamp'])       #'Timestamp'를 날짜값으로 변경

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
    """

    def input_logfile(self):
        #self.logfile_path = input("logfile path: ")
        self.logfile_path = '221209_HISTORY_test.xls'
        self.logdf = pd.read_excel(self.logfile_path)
        self.logdf['ChangeDate'] = pd.to_datetime(self.logdf['ChangeDate'])

        # 로그 파일 시각화
    def visualization(self):
        tmpdf = self.logdf.loc[self.logdf['ModifyType'].isin(['0', '2', '3'])]
        self.visualdf = tmpdf[['ChangeDate', 'ModifyType']]  # timestamp와 행위기록만 추출
        self.visualdf['ChangeDate'] = pd.to_datetime(self.visualdf['ChangeDate'])

        grouped = self.visualdf.groupby(['ChangeDate', 'ModifyType']).size().unstack(fill_value=0)
        grouped = grouped.reset_index('ChangeDate')

        counts = grouped.groupby(pd.Grouper(key='ChangeDate', freq='H')).sum()
        # Plot the results
        counts.plot(kind='bar')
        # Add axis labels and title
        plt.xlabel('Hour')
        plt.ylabel('Count')
        plt.title('Counts of ModifyType values per hour')
        plt.yticks(np.arange(0,10,1))
        # 그래프 그리기
        plt.show()

#테스트
test = LogTimeline()
test.input_logfile()
test.visualization()