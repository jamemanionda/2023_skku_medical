import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np
from datetime import datetime
import glob
import re
import os
import getpass
from tabulate import tabulate
import socket

class ViewRexLogDataFrame():
    def __init__(self):
        self.viewrexlogfile_folder = ''
        self.viewrexlog_dataframe = pd.DataFrame(columns=['Computer Name', 'IP Address', 'Time', 'Action', 'Explaination'])
        self.index = 0
        self.viewrexlogfile_folder = 'C:\\TechHeim\\ViewRex3\\Log'      #로그 파일이 저장되는 기본 경로
        self.computer_name = socket.gethostname()
        self.computer_ip = socket.gethostbyname(self.computer_name)
    #'C:\\'+'컴퓨터이름'+''
    #모든 ViewRex 로그 파일을 불러옴
    def input_viewrexlogfile(self):
        if True:        #Default 경로가 아닌 다른 경로에 파일이 저장되어 있을 경우, 조건문 추가 필요
            self.viewrexlogfile_folder = 'C:\\Users\\skku-dfl\\OneDrive - 성균관대학교\\문서\\SKKU_DFL\\DICOM\\Log'    #실제 로그파일의 폴더를 받을 수 있도록 변경할 것
        self.viewrexlogfile_path = self.viewrexlogfile_folder + "\\ViewRex.exe_*.log"
        for logfile in glob.glob(self.viewrexlogfile_path):
            filename = os.path.basename(logfile)
            with open(logfile, 'r', encoding='UTF-8') as file:
                for line in file:
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
                        Explaination = text[4]

                    if 'Modify Dicom infomation' in line:
                        self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, Time, 'Modify', Explaination]
                        self.index += 1

                    elif 'FROM StudyInformation' in line:
                        self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, Time, 'Select', Explaination]
                        self.index += 1

                    elif 'FROM Patient' in line:
                        self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, Time, 'Select', Explaination]
                        self.index += 1

                    elif 'Export File Path' in line:
                        self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, Time, 'Export', Explaination]
                        self.index += 1

                    #else:
                        #self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, None, None, Explaination]
                        #self.index += 1

        self.viewrexlog_dataframe['Time'] = pd.to_datetime(self.viewrexlog_dataframe['Time'])
        self.viewrexlog_resultdf = self.viewrexlog_dataframe.groupby(['Computer Name', 'IP Address', pd.Grouper(key='Time', freq='D'), 'Action'])['Action'].agg(['count'])
        pd.set_option('display.max_columns', None)
        #pd.set_option('display.max_rows', None)

        #print(self.viewrexlog_resultdf)
        #tmpsdf = tmpsdf.reset_index('Time')

        #testcount = self.viewrexdf_select.resample('D', on='Time').count()
        #print(testcount)

    #excel로 추출
    def export_log_to_excel(self):
        file_names = os.listdir()
        today = datetime.today().strftime("%Y%m%d")
        viewrexlog_filename = 'ViewRexLog_' + str(today)
        tempviewrex_filename = viewrexlog_filename
        filenum = 2
        while True:
            if tempviewrex_filename + '.xlsx' not in file_names:
                self.viewrexlog_resultdf.to_excel(tempviewrex_filename + '.xlsx', encoding='cp949')
                break
            else:
                tempviewrex_filename = viewrexlog_filename + '(' + str(filenum) + ')'
                filenum += 1

test = ViewRexLogDataFrame()
test.input_viewrexlogfile()
#test.export_log_to_excel()