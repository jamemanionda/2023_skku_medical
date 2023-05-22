import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np
import datetime
import glob
import re
import os
import getpass

#ViewRex 로그 파일 타임라인 제작
class ViewRexLogTimeline():
    def __init__(self):
        self.viewrexlogfile_folder = ''
        self.viewrexdf_modify = pd.DataFrame(columns=['Time'])#, 'Number', 'Action'])
        self.viewrexdf_select = pd.DataFrame(columns=['Time'])#, 'Number', 'Action'])
        self.viewrexdf_export = pd.DataFrame(columns=['Time'])#, 'Number', 'Action'])
        self.mindex = 0
        self.sindex = 0
        self.eindex = 0
        self.viewrexlogfile_folder = 'C:\\TechHeim\\ViewRex3\\Log'      #로그 파일이 저장되는 기본 경로
    #'C:\\'+'컴퓨터이름'+''
    #모든 ViewRex 로그 파일을 불러옴
    def input_viewrexlogfile(self):
        if True:        #Default 경로가 아닌 다른 경로에 파일이 저장되어 있을 경우, 조건문 추가 필요
            self.viewrexlogfile_folder = 'C:\\Users\\skku-dfl\\OneDrive - 성균관대학교\\문서\\SKKU_DFL\\DICOM\\Log'    #실제 로그파일의 폴더를 받을 수 있도록 변경할 것
        self.viewrexlogfile_path = self.viewrexlogfile_folder + "\\ViewRex.exe_*.log"
        for logfile in glob.glob(self.viewrexlogfile_path):
            with open(logfile, 'r', encoding='UTF-8') as file:
                for line in file:
                    #if line == '\n':
                    #    continue
                    text = line.split(' ', 4)
                    if len(text) <= 4:
                        continue
                    if text[0] != '':
                        if text[1] == '오후':
                            text[1] = 'PM'
                        elif text[1] == '오전':
                            text[1] = 'AM'

                        Time = text[0] + ' ' + text[2] + ' ' + text[1]
                        Number = text[3]
                        Action = text[4]

                    if 'Modify Dicom infomation' in line:
                        self.viewrexdf_modify.loc[self.mindex] = [Time]#, modifyNumber, modifyAction]
                        self.mindex += 1

                    elif 'FROM StudyInformation' in line:
                        self.viewrexdf_select.loc[self.sindex] = [Time]#, selectNumber, selectAction]
                        self.sindex += 1

                    elif 'FROM Patient' in line:
                        self.viewrexdf_select.loc[self.sindex] = [Time]  # , selectNumber, selectAction]
                        self.sindex += 1

                    elif 'Export File Path' in line:
                        self.viewrexdf_export.loc[self.eindex] = [Time]#, exportNumber, exportAction]
                        self.eindex += 1

        #pd.set_option('display.max_columns', None)
        #pd.set_option('display.max_rows', None)
        #print(self.viewrexdf_select)
        self.viewrexdf_modify['Time'] = pd.to_datetime(self.viewrexdf_modify['Time'])
        self.viewrexdf_select['Time'] = pd.to_datetime(self.viewrexdf_select['Time'])
        self.viewrexdf_export['Time'] = pd.to_datetime(self.viewrexdf_export['Time'])
        tmpmdf = self.viewrexdf_modify['Time'].value_counts()
        tmpsdf = self.viewrexdf_select['Time'].value_counts()
        tmpedf = self.viewrexdf_export['Time'].value_counts()
        #tmpdf = tmpdf.reset_index('Time')

        #print(tmpmdf)

        tmpmdf.plot(kind='line', figsize=(12, 7), color='Red')
        tmpsdf.plot(kind='line', figsize=(12, 7), color='Green')
        tmpedf.plot(kind='line', figsize=(12, 7), color='Blue')
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.show()



test = ViewRexLogTimeline()
test.input_viewrexlogfile()