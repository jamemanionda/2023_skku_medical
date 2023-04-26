import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np
import datetime

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class = uic.loadUiType('History_Timeline.ui')[0]
#로그 시각화
class History_Timeline(QMainWindow, form_class):
    #초기화
    def __init__(self):
        self.historyfile_path = ''
        self.historydf = pd.DataFrame()
        self.visualdf = pd.DataFrame()
        self.input_historyfile()
        super().__init__()
        self.setupUi(self)


        self.OKbutton.clicked.connect(self.accept)
        self.Cancelbutton.clicked.connect(self.reject)


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
    #로그 파일 불러오기
    def input_historyfile(self):
        #self.historyfile_path = input("historyfile path: ")
        #로그 파일 경로
        self.historyfile_path = '221209_HISTORY_test.xls'
        self.historydf = pd.read_excel(self.historyfile_path)
        #로그 DataFrame 생성
        self.historydf['ChangeDate'] = pd.to_datetime(self.historydf['ChangeDate'])

        # 로그 파일 시각화
    def visualization(self, a=None, b=None):
        #a는 시작지점, b는 종료지점
        #a만 설정할 때는 상관없지만 b만 설정하기 위해서는 a에 None이 따로 입력되어야함

        #로그 DataFrame에서 필요한 데이터 추출
        tmpdf = self.historydf.loc[self.historydf['ModifyType'].isin(['0', '2', '3'])]
        self.visualdf = tmpdf[['ChangeDate', 'ModifyType']]

        #날짜 정보를 날짜 형식으로 변환
        self.visualdf['ChangeDate'] = pd.to_datetime(self.visualdf['ChangeDate'])

        #그룹화를 위해 DataFrame 세팅
        grouped = self.visualdf.groupby(['ChangeDate', 'ModifyType']).size().unstack(fill_value=0)
        grouped = grouped.reset_index('ChangeDate')

        #동일한 시간대로 그룹화하여 행위 횟수 카운트
        counts = grouped.groupby(pd.Grouper(key='ChangeDate', freq='H')).sum()

        #타임라인 범위 입력 시 범위추출
        if a is not None or b is not None:
            counts = counts[a:b]

        #그래프를 바 형태로 출력
        counts.plot(kind='bar', figsize=(12, 7))
        ax = plt.gca()

        #그래프 설정
        plt.xlabel('Hour')      #x축 이름
        plt.ylabel('Count')     #y축 이름
        plt.title('Counts of ModifyType values per hour')       #그래프 이름
        plt.xticks(rotation=20)     #x축 값 돌리기
        plt.ylim(0,10)       #y축 정수 표기
        plt.legend(['Delete','Edit','Save'])            #범례 이름 변경

        #눈금선 설정
        ax.xaxis.set_major_locator(MultipleLocator(6))      #주눈금선
        ax.xaxis.set_minor_locator(MultipleLocator(1))      #보조눈금선
        ax.tick_params(length=5, width=1)                   #눈금선 길이 및 두께 조절

        # 그래프 그리기
        plt.show()


    def accept(self):
        startdate = None
        enddate = None
        starttmp = self.Timeline_Date_Start.dateTime()
        startdate = starttmp.toString("yyyy-MM-dd HH:mm")
        endtmp = self.Timeline_Date_End.dateTime()
        enddate = endtmp.toString("yyyy-MM-dd HH:mm")

        if startdate == enddate:
            startdate = None
            enddate = None

        self.visualization(startdate, enddate)

    def reject(self):
        exit()
#테스트

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = History_Timeline()
    test.show()
    app.exec_()

#test = LogTimeline()
#test.input_logfile()
#test.visualization(None,'2022-12-08 12:00')
#print(type('2022-12-08 12:00'))