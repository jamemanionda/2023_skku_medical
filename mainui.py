# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(874, 532)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.file_isForgery_label = QLabel(self.centralwidget)
        self.file_isForgery_label.setObjectName(u"file_isForgery_label")
        self.file_isForgery_label.setGeometry(QRect(30, 40, 111, 16))
        self.file_Forgery_Position_label = QLabel(self.centralwidget)
        self.file_Forgery_Position_label.setObjectName(u"file_Forgery_Position_label")
        self.file_Forgery_Position_label.setGeometry(QRect(30, 70, 111, 16))
        self.file_time_label = QLabel(self.centralwidget)
        self.file_time_label.setObjectName(u"file_time_label")
        self.file_time_label.setGeometry(QRect(30, 100, 91, 16))
        self.dicomView = QGraphicsView(self.centralwidget)
        self.dicomView.setObjectName(u"dicomView")
        self.dicomView.setGeometry(QRect(30, 160, 371, 321))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 140, 61, 16))
        self.dicomTags_lable = QLabel(self.centralwidget)
        self.dicomTags_lable.setObjectName(u"dicomTags_lable")
        self.dicomTags_lable.setGeometry(QRect(650, 140, 61, 16))
        self.dicomTags = QTextBrowser(self.centralwidget)
        self.dicomTags.setObjectName(u"dicomTags")
        self.dicomTags.setGeometry(QRect(650, 160, 211, 321))
        self.fileSelect = QPushButton(self.centralwidget)
        self.fileSelect.setObjectName(u"fileSelect")
        self.fileSelect.setEnabled(True)
        self.fileSelect.setGeometry(QRect(30, 10, 91, 23))
        self.fileSelect.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(420, 140, 61, 16))
        self.file_isForgery_text = QLabel(self.centralwidget)
        self.file_isForgery_text.setObjectName(u"file_isForgery_text")
        self.file_isForgery_text.setGeometry(QRect(140, 40, 261, 16))
        self.file_Forgery_Position_text = QLabel(self.centralwidget)
        self.file_Forgery_Position_text.setObjectName(u"file_Forgery_Position_text")
        self.file_Forgery_Position_text.setGeometry(QRect(140, 70, 261, 16))
        self.file_time_text = QLabel(self.centralwidget)
        self.file_time_text.setObjectName(u"file_time_text")
        self.file_time_text.setGeometry(QRect(130, 100, 261, 16))
        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(410, 160, 221, 321))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 874, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        self.retranslateUi(MainWindow)
        #self.fileSelect.clicked.connect(MainWindow.openFile)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Forensic Tool", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.file_isForgery_label.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c \uc704\ubcc0\uc870 \uc5ec\ubd80", None))
        self.file_Forgery_Position_label.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c \uc704\ubcc0\uc870 \uc704\uce58", None))
        self.file_time_label.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0ac \uc2dc\uac04", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\uc601\uc0c1 \ud654\uba74", None))
        self.dicomTags_lable.setText(QCoreApplication.translate("MainWindow", u"\ud0dc\uadf8 \ubd84\ub958", None))
        self.fileSelect.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c \uc120\ud0dd", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\uc601\uc0c1 \uc815\ubcf4", None))
        self.file_isForgery_text.setText("")
        self.file_Forgery_Position_text.setText("")
        self.file_time_text.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

