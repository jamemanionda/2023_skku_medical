import pymssql
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QComboBox, QInputDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PACS_DB import Ui_Dialog

class MyApp(QDialog, Ui_Dialog):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        server = 'PACSSERVER'
        database = 'ViewRex'

        cnxn = pymssql.connect(server='PACSSERVER', database='ViewRex', charset='utf8')
        cursor = cnxn.cursor()

        cursor.execute('IF OBJECT_ID(\'V_ForensicQuery\', \'V\') IS NOT NULL DROP VIEW V_ForensicQuery')
        cursor.execute('CREATE VIEW V_ForensicQuery AS SELECT TOP 100 PERCENT A.PatientID, A.LastName, A.Sex, A.BirthDate, B.StudyName, B.BodyPartName, B.StudyInstanceUID, B.StudyDate, B.SaveDate, C.UserID, C.TableName, C.ModifyType, C.ChangeDate, LEAD(C.ChangeDate) OVER(ORDER BY C.ChangeDate) AS DATE2, C.Description FROM Patient AS A LEFT OUTER JOIN StudyInformation AS B ON A.PatientID = B.PatientID LEFT OUTER JOIN History AS C ON A.PatientID = C.PatientID LEFT OUTER JOIN LogonUserInformation AS D ON D.TimeDate BETWEEN CONVERT(datetime, C.ChangeDate) AND CONVERT(datetime, C.ChangeDate)  ORDER BY C.ChangeDate')

        cursor.execute('SELECT * FROM V_ForensicQuery')
        columns = [column[0] for column in cursor.description]

        rows = cursor.fetchall()
        self.df = pd.DataFrame(rows, columns=columns)
        cnxn.close()

        self.columns = self.df.columns.tolist()
        self.DBcolumn_comboBox.addItem("")
        self.DBcolumn_comboBox.addItems(self.columns)
        self.DBcolumn_comboBox.activated[str].connect(self.filter_df)

        self.filter_df("")

        self.sort_order = Qt.AscendingOrder
        self.DatabaseTable.setSortingEnabled(True)
        self.DatabaseTable.horizontalHeader().sectionClicked.connect(self.sort_table)

    def filter_df(self, selected_column):
        try:
            if selected_column.strip() == "":
                filtered_df = self.df
            else:
                items = sorted(self.df[selected_column].astype(str).unique())
                selected_value, ok = QInputDialog.getItem(self, 'Input Dialog', f'{selected_column} 값 선택:', items, editable=False)
                if ok:
                    filtered_df = self.df[self.df[selected_column].astype(str) == selected_value]
                else:
                    filtered_df = pd.DataFrame(columns=self.df.columns).astype(str)

            if filtered_df.empty:
                self.clear_table()
                return
        except Exception as e:
            print("오류가 발생했습니다: ", e)
        else:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(self.df.columns)
            for _, row in filtered_df.iterrows():
                items = [QStandardItem(str(i)) for i in row]
                model.appendRow(items)
            self.DatabaseTable.setModel(model)

    def clear_table(self):
        model = QStandardItemModel()
        self.DatabaseTable.setModel(model)

    def sort_table(self, column_index):
        header = self.DatabaseTable.horizontalHeader()
        self.sort_order = self.sort_order == Qt.AscendingOrder
        header.setSortIndicator(column_index, self.sort_order)
        self.DatabaseTable.sortByColumn(column_index, self.sort_order)


app = QApplication(sys.argv)
ui = MyApp()
ui.show()
sys.exit(app.exec_())
