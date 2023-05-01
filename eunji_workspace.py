import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import pydicom

class DicomView(QGraphicsView):
    def __init__(self):
        super().__init__()

    def setDicomImage(self, image):
        scene = QGraphicsScene(self)
        scene.addPixmap(QPixmap.fromImage(image))
        self.setScene(scene)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("DICOM Viewer")

        self.dicomView = DicomView()
        self.setCentralWidget(self.dicomView)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")

        openAction = QAction("Open DICOM", self)
        openAction.triggered.connect(self.openDicom)
        fileMenu.addAction(openAction)

    def openDicom(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open DICOM", "", "DICOM Files (*.dcm)", options=options)
        if fileName:
            dicomData = pydicom.dcmread(fileName)
            dicomImage = QImage(dicomData.pixel_array, dicomData.pixel_array.shape[1], dicomData.pixel_array.shape[0], QImage.Format_Grayscale8)
            self.dicomView.setDicomImage(dicomImage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())