import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout


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
        self.show()

    def pacsClicked(self):
        print('PACS button clicked')

    def dicomClicked(self):
        print('DICOM button clicked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
