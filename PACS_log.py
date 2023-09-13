import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import glob
import re
import os
import sys
from tabulate import tabulate
import socket
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pacs_main

form_class = uic.loadUiType('pacs_log.ui')[0]

class ViewRexLogDataFrame(QMainWindow, form_class):
    def __init__(self):
        self.pacs_ui = uic.loadUi('PACS.ui')
        self.pacs_ui.Logtable.setVisible(False)
        self.viewrexlogfile_folder = ''
        self.viewrexlog_dataframe = pd.DataFrame(columns=['Time', 'Action', 'Explaination'])
        self.index = 0
        self.viewrexlogfile_folder = 'C:\\TechHeim\\ViewRex3\\Log'      #로그 파일이 저장되는 기본 경로
        self.computer_name = socket.gethostname()
        self.computer_ip = socket.gethostbyname(self.computer_name)
        self.date_valid = True
        super().__init__()
        self.setupUi(self)

        #self.df = self.input_viewrexlogfile()
        #self.create_table_widget(self.df, widget = self.tableWidget)

        self.auto_button.clicked.connect(self.autoExtract)
        self.manual_button.clicked.connect(self.manualExtract)
        self.Detail_view_button.clicked.connect(self.detail_information)
        self.OK_button.clicked.connect(self.accept)
        self.Exit_button.clicked.connect(self.reject)

    #'C:\\'+'컴퓨터이름'+''
    #모든 ViewRex 로그 파일을 불러옴
    def autoExtract(self):
        lasttime = 0
        if True:        #Default 경로가 아닌 다른 경로에 파일이 저장되어 있을 경우, 조건문 추가 필요
            self.viewrexlogfile_folder = 'C:\\Users\\skku-dfl\\OneDrive - 성균관대학교\\문서\\SKKU_DFL\\DICOM\\Log'    #실제 로그파일의 폴더를 받을 수 있도록 변경할 것
        self.viewrexlogfile_path = self.viewrexlogfile_folder + "\\ViewRex.exe_*.log"
        textline = []
        for logfile in glob.glob(self.viewrexlogfile_path):
            filename = os.path.basename(logfile)
            with open(logfile, 'r', encoding='UTF-8') as file:
                for line in file:
                    textline.append(line)
                    if line == '\n':
                        for i in range(len(textline)-1):
                            textline[i] = textline[i].strip()
                        line = ' '.join(textline)
                        textline = []
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
                            explaination = text[4]
                            temp = explaination.split(' ', 3)
                            Explaination = temp[3]
                            if lasttime == Time:
                                continue
                            else:
                                lasttime = Time

                        if 'Modify Dicom infomation' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time, 'Modify', Explaination]
                            self.index += 1

                        elif 'FROM StudyInformation' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time, 'Select', Explaination]
                            self.index += 1

                        elif 'FROM Patient' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time, 'Select', Explaination]
                            self.index += 1

                        elif 'Export File Path' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time, 'Export', Explaination]
                            self.index += 1

                        #else:
                            #self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, None, None, Explaination]
                            #self.index += 1

        #self.viewrexlog_dataframe.index = self.viewrexlog_dataframe.index + 1
        self.viewrexlog_dataframe['Time'] = pd.to_datetime(self.viewrexlog_dataframe['Time'])
        self.viewrexlog_resultdf = self.viewrexlog_dataframe.groupby([pd.Grouper(key='Time', freq='D'), 'Action'])['Action'].agg(['count'])
        pd.set_option('display.max_columns', None)

        self.create_table_widget(self.viewrexlog_resultdf, widget = self.tableWidget)
        self.tossview = self.viewrexlog_resultdf
        print(self.tossview)

    def manualExtract(self):
        fname = QFileDialog.getOpenFileNames(self, "File Load", 'C:\\TechHeim\\ViewRex3\\Log',
                                             'All File(*);; Text File(*.txt);; Log file(*.log)')

        textline = []
        for logfile in fname[0]:
            logfile = logfile.replace('/', '\\')
            with open(logfile, 'r', encoding='UTF-8') as file:
                for line in file:
                    textline.append(line)
                    if line == '\n':
                        for i in range(len(textline) - 1):
                            textline[i] = textline[i].strip()
                        line = ' '.join(textline)
                        textline = []
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
                            self.viewrexlog_dataframe.loc[self.index] = [Time,
                                                                         'Modify', Explaination]
                            self.index += 1

                        elif 'FROM StudyInformation' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time,
                                                                         'Select', Explaination]
                            self.index += 1

                        elif 'FROM Patient' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time,
                                                                         'Select', Explaination]
                            self.index += 1

                        elif 'Export File Path' in line:
                            self.viewrexlog_dataframe.loc[self.index] = [Time,
                                                                         'Export', Explaination]
                            self.index += 1

                        # else:
                        # self.viewrexlog_dataframe.loc[self.index] = [self.computer_name, self.computer_ip, None, None, Explaination]
                        # self.index += 1

        # self.viewrexlog_dataframe.index = self.viewrexlog_dataframe.index + 1
        self.viewrexlog_dataframe['Time'] = pd.to_datetime(self.viewrexlog_dataframe['Time'])
        self.viewrexlog_resultdf = self.viewrexlog_dataframe.groupby([pd.Grouper(key='Time', freq='D'), 'Action'])[
            'Action'].agg(['count'])
        pd.set_option('display.max_columns', None)

        self.create_table_widget(self.viewrexlog_resultdf, widget=self.tableWidget)
        self.tossview = self.viewrexlog_resultdf
        print(self.viewrexlog_resultdf)

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
                #self.viewrexlog_dataframe.to_excel(tempviewrex_filename + '.xlsx', encoding='cp949')
                break
            else:
                tempviewrex_filename = viewrexlog_filename + '(' + str(filenum) + ')'
                filenum += 1


    def detail_information(self):
        action = str(self.chooseaction.currentText())
        sd = self.sdate.dateTime()
        ed = self.edate.dateTime()
        startdate = sd.toString('yyyy-MM-dd HH:mm')
        enddate = ed.toString('yyyy-MM-dd HH:mm')


        if sd < ed:
            temp_df = self.viewrexlog_dataframe.set_index('Time')
            temp_df = temp_df[startdate:enddate]
            detailview_df = temp_df[temp_df['Action'] == action]
            self.tossview = detailview_df
            #print(detailview_df)
            self.create_table_widget(detailview_df, widget=self.tableWidget)

            print(detailview_df)

    def create_table_widget(self, df, widget):
        widget.setRowCount(len(df.index))
        widget.setColumnCount(len(df.columns))
        widget.setHorizontalHeaderLabels(df.columns)
        widget.setVerticalHeaderLabels([str(item) for item in df.index])

        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index, col_index, item)

    def accept(self):
        try:
            self.b = pacs_main.Pacs_main()  # aaaaa 클래스의 인스턴스 생성
            self.b.show_log(self.tossview)
            self.b.show()  # 생성된 인스턴스의 show() 메소드 호출
        except Exception as e:
            print(f"Error occurred: {e}")
        self.close()

    def reject(self):
        self.close()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = ViewRexLogDataFrame()
    test.show()
    app.exec_()
