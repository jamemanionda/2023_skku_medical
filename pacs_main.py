import glob
import re
import os
import sys
from tabulate import tabulate
import socket
from PyQt5.QtWidgets import *
from PyQt5 import uic
import PACS_log
import PACS_DB

form_class = uic.loadUiType('PACS.ui')[0]

class Pacs_main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Logtable = self.findChild(QTableWidget, 'Logtable')

        self.DB_btn.clicked.connect(self.connect_DB)
        self.Log_btn.clicked.connect(self.connect_Log)

    def connect_DB(self):
        self.DB = PACS_DB.Ui_Dialog()
        self.DB.show()
        self.close()
    def connect_Log(self):
        self.log = PACS_log.ViewRexLogDataFrame()
        self.log.show()
        self.close()
    def show_log(self, df):
        self.create_table_widget(df, widget=self.Logtable)


    def show_db(self, df):
        self.create_table_widget(df, widget=self.DBtable)

    def accept(self):
        exit()

    def reject(self):
        self.close()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = Pacs_main()
    test.show()
    app.exec_()