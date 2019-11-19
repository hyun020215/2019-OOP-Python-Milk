import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import facebook_parser as fbps


class WebCrawl(QThread):

    finished = pyqtSignal(list)

    def __init__(self, begin, finish):
        QThread.__init__(self)
        self.begin = begin
        self.finish = finish

    def run(self) -> None:
        result = fbps.post_crawl(self.begin, self.finish)
        self.finished.emit(result)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # set up UI
        period_label = QHBoxLayout()
        period_label.addWidget(QLabel('검색 기간', self))
        period_label.addStretch()

        self.period_start = QDateEdit(self)
        self.period_end = QDateEdit(self)

        period = QHBoxLayout()
        period.addWidget(self.period_start)
        period.addWidget(QLabel('~', self))
        period.addWidget(self.period_end)

        search_button = QPushButton('검색', self)
        search_button.clicked.connect(self.period_check)

        search_button_layout = QHBoxLayout()
        search_button_layout.addStretch()
        search_button_layout.addWidget(search_button)

        self.period_alert = QLabel('검색 기간이 잘못되었습니다.', self)
        self.period_alert.setObjectName('period_alert')
        self.period_alert.setStyleSheet('QLabel#period_alert {color: red}')
        self.period_alert.hide()

        set_condition = QVBoxLayout()
        set_condition.addLayout(period_label)
        set_condition.addLayout(period)
        set_condition.addLayout(search_button_layout)
        set_condition.addWidget(self.period_alert)
        set_condition.addStretch()
        self.post_crawling = WebCrawl(self.period_start, self.period_end)
        self.post_crawling.finished.connect(self.update_search_result_list)

        self.result_list = QListWidget(self)
        self.no_result = QLabel('검색 결과가 없습니다.', self)
        self.no_result.setObjectName('no_result')
        self.no_result.setStyleSheet('QLabel#no_result {color: red}')
        self.no_result.hide()
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        self.progress.hide()

        search_result = QVBoxLayout()
        search_result.addWidget(QLabel('검색 결과', self))
        search_result.addWidget(self.progress)
        search_result.addWidget(self.no_result)
        search_result.addWidget(self.result_list)

        search = QHBoxLayout()
        search.addLayout(search_result)
        search.addLayout(set_condition)
        search.setStretchFactor(search_result, 1)
        search.setStretchFactor(set_condition, 0)

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
        reply = QMessageBox.question(self, 'Message', '정말 프로그램을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def period_check(self):
        if self.period_start.date() > self.period_end.date():
            self.period_alert.show()
        else:
            self.period_alert.hide()
            self.result_list.clear()
            self.progress.show()
            self.post_crawling.start()

    @ pyqtSlot(list)
    def update_search_result_list(self, result):
        if not result:
            self.no_result.show()
        else:
            self.progress.hide()
            self.result_list.addItems(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
