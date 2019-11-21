import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import facebook_parser as fbps


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # set up UI
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
        set_condition.addWidget(QLabel('검색 기간', self))
        set_condition.addLayout(period)
        set_condition.addLayout(search_button_layout)
        set_condition.addWidget(self.period_alert)
        set_condition.addStretch()
        set_condition.addWidget(QLabel('게시물 내용', self))

        self.post_crawling = PostCrawl(self)
        self.post_crawling.finished.connect(self.update_search_result_list)

        sort_by = QComboBox(self)
        sort_by.addItems(['게시 일자', '공감 수', '댓글 수'])
        sort_by.currentIndexChanged.connect(self.set_sort_method)

        search_result_label1 = QHBoxLayout()
        search_result_label1.addWidget(QLabel('검색 결과', self))
        search_result_label1.addStretch()
        search_result_label1.addWidget(QLabel('정렬 기준', self))
        search_result_label1.addWidget(sort_by)

        self.no_result = QLabel('검색 결과가 없습니다.', self)
        self.no_result.setObjectName('no_result')
        self.no_result.setStyleSheet('QLabel#no_result {color: red}')
        self.no_result.hide()
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        self.progress.hide()
        self.loading_message = QLabel('검색 중... (검색 기간에 따라 시간이 소요될 수도 있습니다.)', self)
        self.loading_message.hide()

        search_result_label2 = QHBoxLayout()
        search_result_label2.addWidget(self.progress)
        search_result_label2.addWidget(self.loading_message)
        search_result_label2.addWidget(self.no_result)
        search_result_label2.addStretch()

        self.post_list = []
        self.result_list = QTableWidget(10, 5, self)
        self.result_list.setHorizontalHeaderLabels(['게시 일자', '내용', '공감 수', '댓글 수', '카테고리'])
        self.result_list.setColumnWidth(0, 100)
        self.result_list.setColumnWidth(1, 250)
        self.result_list.setColumnWidth(2, 50)
        self.result_list.setColumnWidth(3, 50)
        self.result_list.setColumnWidth(4, 100)
        self.result_list.cellDoubleClicked.connect(self._post_double_clicked)

        self.current_sort_method = lambda post: post.date

        search_result = QVBoxLayout()
        search_result.addLayout(search_result_label1)
        search_result.addLayout(search_result_label2)
        search_result.addWidget(self.result_list)

        search = QHBoxLayout()
        search.addLayout(search_result)
        search.addLayout(set_condition)
        search.setStretchFactor(search_result, 1)
        search.setStretchFactor(set_condition, 0)

        self.resize(805, 600)
        self.center()
        self.setWindowTitle("SASA Bamboo Analyzer")
        self.setWindowIcon(QIcon('images/icon.png'))

        # self.lineEdit = QLineEdit()
        # self.pushButton = QPushButton("차트그리기", self)
        # self.pushButton.clicked.connect(self.push_button_clicked)

        # self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)

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

        background = QImage('images/background.png')
        palette = QPalette()
        palette.setBrush(10, QBrush(background.scaled(QSize(805, 600))))
        self.setPalette(palette)

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
            self.no_result.hide()
            self.progress.show()
            self.loading_message.show()
            self.post_crawling.start()

    @ pyqtSlot(list)
    def update_search_result_list(self, post_list: list):
        self.post_list = post_list
        self.progress.hide()
        self.loading_message.hide()
        self.no_result.hide()
        self.result_list.clearContents()
        if not post_list:
            self.no_result.show()
        else:
            for index, post in enumerate(sorted(post_list, key=self.current_sort_method, reverse=True)):
                date = QTableWidgetItem(post.date)
                text = QTableWidgetItem(post.text)
                like = QTableWidgetItem(str(post.like))
                comment = QTableWidgetItem(str(post.comment))
                category = QTableWidgetItem(', '.join(post.get_category()))

                date.setTextAlignment(Qt.AlignCenter)
                text.setTextAlignment(Qt.AlignCenter)
                like.setTextAlignment(Qt.AlignCenter)
                comment.setTextAlignment(Qt.AlignCenter)
                category.setTextAlignment(Qt.AlignCenter)

                self.result_list.setItem(index, 0, date)
                self.result_list.setItem(index, 1, text)
                self.result_list.setItem(index, 2, like)
                self.result_list.setItem(index, 3, comment)
                self.result_list.setItem(index, 4, category)

    def set_sort_method(self, idx: int):
        if idx == 0:
            self.current_sort_method = lambda post: post.date
        elif idx == 1:
            self.current_sort_method = lambda post: post.like
        else:
            self.current_sort_method = lambda post: post.comment

        self.update_search_result_list(self.post_list)

    def _post_double_clicked(self, row, col):
        if col == 1:
            print(self.result_list.currentItem().text())


class PostCrawl(QThread):

    finished = pyqtSignal(list)

    def __init__(self, current_window: MyWindow):
        QThread.__init__(self)
        self.window = current_window

    def run(self) -> None:
        result = fbps.post_crawl(self.window.period_start, self.window.period_end)
        self.finished.emit(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
