from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WindowWithExtraFunctions(QWidget):
    def __init__(self):
        super().__init__()

        background = QImage('images/background.png')
        palette = QPalette()
        palette.setBrush(10, QBrush(background.scaled(self.size())))  # window OS에서 작동함
        self.setPalette(palette)
        self.setWindowIcon(QIcon('images/icon.png'))

    def center(self):
        position = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        position.moveCenter(center_point)
        self.move(position.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '창을 닫으시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
