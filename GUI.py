"""
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QToolTip, QMainWindow, QAction, qApp, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


class MyApp(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('images/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.statusBar().showMessage('Ready')

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(300, 150)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.resize(400, 200)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_UI()

    def set_up_UI(self):
        period_start = QDateEdit(self)
        period_end = QDateEdit(self)

        period = QHBoxLayout()
        period.addStretch(1)
        period.addWidget(period_start)
        period.addWidget(QLabel('~', self))
        period.addWidget(period_end)
        period.addStretch(1)

        search_button = QPushButton('검색', self)

        set_condition = QVBoxLayout()
        set_condition.addLayout(period)
        set_condition.addWidget(search_button)
        set_condition.addStretch(8)

        result_list = QListView(self)

        search_result = QVBoxLayout()
        search_result.addWidget(QLabel('검색 결과', self))
        search_result.addWidget(result_list)

        search = QHBoxLayout()
        search.addStretch(1)
        search.addLayout(search_result)
        search.addStretch(1)
        search.addLayout(set_condition)
        search.addStretch(1)

        self.resize(1200, 600)
        self.center()
        self.setWindowTitle("SASA Bamboo Analyzer")
        self.setWindowIcon(QIcon('images/icon.png'))

        # self.lineEdit = QLineEdit()
        # self.pushButton = QPushButton("차트그리기", self)
        # self.pushButton.clicked.connect(self.push_button_clicked)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        # left_layout = QVBoxLayout()
        # left_layout.addWidget(self.canvas)
        #
        # # Right Layout
        # right_layout = QVBoxLayout()
        # right_layout.addWidget(self.lineEdit)
        # right_layout.addWidget(self.pushButton)
        # right_layout.addStretch(1)
        #
        # layout = QHBoxLayout()
        # layout.addLayout(left_layout)
        # layout.addLayout(right_layout)
        # layout.setStretchFactor(left_layout, 1)
        # layout.setStretchFactor(right_layout, 0)

        # self.setLayout(layout)

        self.setLayout(search)

    # def push_button_clicked(self):
    #     print(self.lineEdit.text())

    def center(self):
        position = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        position.moveCenter(center_point)
        self.move(position.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
