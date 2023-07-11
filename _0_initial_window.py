import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMessageBox, QApplication

from dicom_main import DicomInformation
from pacs_main import Pacs_main
from qt_material import apply_stylesheet

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        pacs_button = QPushButton('PACS', self)
        pacs_button.clicked.connect(self.pacsClicked)

        dicom_button = QPushButton('DICOM', self)
        dicom_button.clicked.connect(self.dicomClicked)

        hbox = QHBoxLayout()
        hbox.addWidget(pacs_button)
        hbox.addWidget(dicom_button)

        self.setLayout(hbox)

        self.setWindowTitle('PACS vs. DICOM')
        self.setGeometry(300, 300, 300, 100)
        self.closeEvent = self.handleCloseEvent


    def pacsClicked(self):
        print('PACS button clicked')
        try:
            self.b = Pacs_main()  # aaaaa 클래스의 인스턴스 생성
            self.b.show()  # 생성된 인스턴스의 show() 메소드 호출
        except Exception as e:
            print(f"Error occurred: {e}")

    def dicomClicked(self):
        print('DICOM button clicked')
        try:
            self.a = DicomInformation()  # aaaaa 클래스의 인스턴스 생성
            self.a.show()  # 생성된 인스턴스의 show() 메소드 호출
        except Exception as e:
            print(f"Error occurred: {e}")



    def handleCloseEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class aaaaa(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('aaaaa')
        self.setGeometry(400, 400, 300, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec()
