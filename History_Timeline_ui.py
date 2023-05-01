# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'History_Timeline.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDialog, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(582, 359)

        self.Cancelbutton = QPushButton(Dialog)
        self.Cancelbutton.setObjectName(u"Cancelbutton")
        self.Cancelbutton.setGeometry(QRect(350, 260, 75, 24))
        self.OKbutton = QPushButton(Dialog)
        self.OKbutton.setObjectName(u"OKbutton")
        self.OKbutton.setGeometry(QRect(270, 260, 75, 24))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 120, 71, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(110, 60, 81, 16))
        self.Timeline_Date_Start = QDateTimeEdit(Dialog)
        self.Timeline_Date_Start.setObjectName(u"Timeline_Date_Start")
        self.Timeline_Date_Start.setGeometry(QRect(110, 80, 194, 22))
        self.Timeline_Date_Start.setDateTime(QDateTime(QDate(2023, 1, 1), QTime(0, 0, 0)))
        self.Timeline_Date_Start.setCalendarPopup(True)
        self.Timeline_Date_End = QDateTimeEdit(Dialog)
        self.Timeline_Date_End.setObjectName(u"Timeline_Date_End")
        self.Timeline_Date_End.setGeometry(QRect(110, 140, 194, 22))
        self.Timeline_Date_End.setDateTime(QDateTime(QDate(2023, 1, 1), QTime(0, 0, 0)))
        self.Timeline_Date_End.setTime(QTime(0, 0, 0))
        self.Timeline_Date_End.setCalendarPopup(True)
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Timeline_Date_End.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy-MM-dd HH:mm", None))
        self.Cancelbutton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.OKbutton.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"End Time", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Start Time", None))
        self.Timeline_Date_Start.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy-MM-dd HH:mm", None))
    # retranslateUi

