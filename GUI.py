import sys

from PyQt5.QtCore import *
from upgrade_window import *

from facebook_parser import *
from graphs import *


class MainWindow(QMainWindow, WindowWithExtraFunctions):
    def __init__(self):
        super().__init__()

        exit_action = QAction(QIcon('images/exit.png'), '종료하기', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('프로그램을 종료합니다.')
        exit_action.triggered.connect(qApp.closeAllWindows)

        print_action = QAction(QIcon('images/print.png'), '출력하기', self)
        print_action.setShortcut('Ctrl+P')
        print_action.setStatusTip('검색 결과를 출력합니다.')
        print_action.triggered.connect(self._print_result)

        save_action = QAction(QIcon('images/save.png'), '저장하기', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('검색 결과를 저장합니다.')
        save_action.triggered.connect(self._save_result)

        draw_graph = QAction(QIcon('images/graph.png'), '그래프', self)
        draw_graph.setShortcut('Ctrl+G')
        draw_graph.setStatusTip('검색 자료를 바탕으로 그래프를 그립니다.')
        draw_graph.triggered.connect(self._open_graph_window)

        edit_keyword = QAction(QIcon('images/edit.png'), '키워드 편집', self)
        edit_keyword.setShortcut('Ctrl+K')
        edit_keyword.setStatusTip('검색된 게시물을 분류하는 키워드를 편집합니다.')
        edit_keyword.triggered.connect(self._open_keyword_window)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        file_menu = menubar.addMenu('파일')
        file_menu.addAction(exit_action)
        file_menu.addAction(print_action)
        file_menu.addAction(save_action)

        statistics_menu = menubar.addMenu('통계')
        statistics_menu.addAction(draw_graph)

        settings_menu = menubar.addMenu('설정')
        settings_menu.addAction(edit_keyword)

        self.post_search_window = MainWidget()
        self.setCentralWidget(self.post_search_window)

        self.statusBar()

        self.resize(900, 600)
        self.center()
        self.setWindowTitle("SASA 대나무숲 분석기")

    def _print_result(self):
        if not self.post_search_window.post_list:
            QMessageBox.information(self, 'Message', '출력할 자료가 없습니다.', QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'Message', '미구현된 기능입니다.', QMessageBox.Ok)

    def _save_result(self):
        if not self.post_search_window.post_list:
            QMessageBox.information(self, 'Message', '저장할 자료가 없습니다.', QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'Message', '미구현된 기능입니다.', QMessageBox.Ok)

    def _open_graph_window(self):
        if not self.post_search_window.post_list:
            QMessageBox.information(self, 'Message', '그래프를 그릴 자료가 없습니다.', QMessageBox.Ok)
        else:
            GraphWindow(self.post_search_window.post_list).exec_()

    @ staticmethod
    def _open_keyword_window():
        KeywordEditWindow().exec_()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # set up UI
        today_ = datetime.datetime.now()
        last_ = today_ - datetime.timedelta(days=7)

        self.period_start = QDateEdit(self)
        self.period_start.setDate(QDate(last_.year, last_.month, last_.day))
        self.period_end = QDateEdit(self)
        self.period_end.setDate(QDate(today_.year, today_.month, today_.day))
        search_button = QPushButton('검색', self)
        search_button.clicked.connect(self.period_check)

        period = QHBoxLayout()
        period.addWidget(self.period_start)
        period.addWidget(QLabel('~', self))
        period.addWidget(self.period_end)
        period.addWidget(search_button)

        self.period_alert = QLabel('검색 기간이 잘못되었습니다.', self)
        self.period_alert.setObjectName('period_alert')
        self.period_alert.setStyleSheet('QLabel#period_alert {color: red}')
        self.period_alert.hide()

        self.post_content = QTextBrowser()

        show_post_content = QVBoxLayout()
        show_post_content.addWidget(QLabel('게시물 내용', self))
        show_post_content.addWidget(self.post_content)

        set_condition = QVBoxLayout()
        set_condition.addWidget(QLabel('검색 기간', self))
        set_condition.addLayout(period)
        set_condition.addWidget(self.period_alert)
        set_condition.addStretch()
        set_condition.addLayout(show_post_content)

        self.post_crawling = PostCrawl(self)
        self.post_crawling.finished.connect(self.update_search_result_list)

        sort_by = QComboBox(self)
        sort_by.addItems(['게시 일자', '공감 수', '댓글 수', '주제'])
        sort_by.currentIndexChanged.connect(self._set_sort_method)

        search_result_label1 = QHBoxLayout()
        search_result_label1.addWidget(QLabel('검색 결과', self))
        search_result_label1.addStretch()
        search_result_label1.addWidget(QLabel('정렬 기준', self))
        search_result_label1.addWidget(sort_by)

        self.no_result = QLabel('검색 결과가 없습니다.', self)
        self.no_result.setObjectName('no_result')
        self.no_result.setStyleSheet('QLabel#no_result {color: red}')
        self.no_result.hide()
        self.no_internet = QLabel('인터넷 연결이 없습니다.', self)
        self.no_internet.setObjectName('no_internet')
        self.no_internet.setStyleSheet('QLabel#no_internet {color: blue}')
        self.no_internet.hide()
        self.no_connection = QLabel('인터넷이 끊겼습니다.', self)
        self.no_connection.setObjectName('no_connection')
        self.no_connection.setStyleSheet('QLabel#no_connection {color: blue}')
        self.no_connection.hide()
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        self.progress.hide()
        self.loading_message = QLabel('검색 중... (검색 기간에 따라 시간이 소요될 수도 있습니다.)', self)
        self.loading_message.hide()

        search_result_label2 = QHBoxLayout()
        search_result_label2.addWidget(self.progress)
        search_result_label2.addWidget(self.loading_message)
        search_result_label2.addWidget(self.no_result)
        search_result_label2.addWidget(self.no_internet)
        search_result_label2.addWidget(self.no_connection)
        search_result_label2.addStretch()

        self.post_list = []
        self.result_list = QTableWidget(10, 5, self)
        self.result_list.setEditTriggers(QTableWidget.NoEditTriggers)
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

        self.setLayout(search)

    def period_check(self):
        if self.period_start.date() > self.period_end.date():
            self.period_alert.show()
        else:
            self.period_alert.hide()
            self.no_result.hide()
            self.no_internet.hide()
            self.no_connection.hide()
            self.progress.show()
            self.loading_message.show()
            self.post_crawling.start()

    @pyqtSlot(list)
    def update_search_result_list(self, post_list: list):
        self.result_list.setRowCount(10)
        self.post_list = post_list
        self.progress.hide()
        self.loading_message.hide()
        self.no_result.hide()
        self.no_internet.hide()
        self.no_connection.hide()
        self.result_list.clearContents()
        if not post_list:
            self.no_result.show()
        elif post_list == ['q']:
            self.no_internet.show()
        elif post_list == ['p']:
            self.no_connection.show()
        else:
            for index, post in enumerate(sorted(post_list, key=self.current_sort_method, reverse=True)):
                date = QTableWidgetItem(post.date)
                text = QTableWidgetItem(post.text)
                like = QTableWidgetItem(str(post.like))
                comment = QTableWidgetItem(str(post.comment))
                category = QTableWidgetItem(', '.join(post.get_category()))

                date.setTextAlignment(Qt.AlignCenter)
                like.setTextAlignment(Qt.AlignCenter)
                comment.setTextAlignment(Qt.AlignCenter)
                category.setTextAlignment(Qt.AlignCenter)

                if self.result_list.rowCount() < len(post_list):
                    self.result_list.insertRow(self.result_list.rowCount())

                self.result_list.setItem(index, 0, date)
                self.result_list.setItem(index, 1, text)
                self.result_list.setItem(index, 2, like)
                self.result_list.setItem(index, 3, comment)
                self.result_list.setItem(index, 4, category)

    def _set_sort_method(self, idx: int):
        if idx == 0:
            self.current_sort_method = lambda post: post.date
        elif idx == 1:
            self.current_sort_method = lambda post: post.like
        elif idx == 2:
            self.current_sort_method = lambda post: post.comment
        else:
            self.current_sort_method = lambda post: post.get_category()

        if self.post_list:
            self.update_search_result_list(self.post_list)

    def _post_double_clicked(self, _, column):
        if column in [1, 4] and self.result_list.currentItem():
            self.post_content.setText(self.result_list.currentItem().text())


class PostCrawl(QThread):
    finished = pyqtSignal(list)

    def __init__(self, current_window: MainWidget):
        QThread.__init__(self)
        self.window = current_window

    def run(self) -> None:
        result = post_crawl(self.window.period_start.text(), self.window.period_end.text())
        self.finished.emit(result)


class GraphWindow(QDialog, WindowWithExtraFunctions):
    def __init__(self, posts):
        super().__init__()

        self.posts = posts
        self.category_check = []

        file = open('category_keywords.pickle', 'rb')
        self.categorized_posts = pickle.load(file)
        for key in self.categorized_posts.keys():
            self.categorized_posts[key] = []
        file.close()

        for post in posts:
            for category in self.categorized_posts.keys():
                if category in post.get_category():
                    self.categorized_posts[category].append(post)

        # set up UI
        draw_line = QRadioButton('날짜별 게시물 증가 추이(꺾은선 그래프)')
        draw_bar = QRadioButton('주제별 게시물 수(막대 그래프)')
        draw_pie = QRadioButton('주제별 게시물 비율(원 그래프)')

        draw_line.clicked.connect(self.show_line_widget)
        draw_bar.clicked.connect(self.show_bar_widget)
        draw_pie.clicked.connect(self.show_pie_widget)

        draw_line.setChecked(True)

        graph_type = QVBoxLayout()
        graph_type.addWidget(draw_line)
        graph_type.addWidget(draw_bar)
        graph_type.addWidget(draw_pie)

        select_graph_type = QGroupBox('그래프 종류')
        select_graph_type.setLayout(graph_type)

        self.select_category = QGroupBox('카테고리')

        self.checkbox_uncheck_alert = QLabel('1개 이상의 주제를 선택해주세요.')
        self.checkbox_uncheck_alert.setObjectName('uncheck_alert')
        self.checkbox_uncheck_alert.setStyleSheet('QLabel#uncheck_alert {color: red}')
        self.checkbox_uncheck_alert.hide()

        check_all = QPushButton('전체 선택')
        check_all.clicked.connect(self.check_all_category)
        uncheck_all = QPushButton('전체 해제')
        uncheck_all.clicked.connect(self.uncheck_all_category)

        button_layout = QHBoxLayout()
        button_layout.addWidget(check_all)
        button_layout.addWidget(uncheck_all)

        select_category_layout = QVBoxLayout()
        select_category_layout.addWidget(self.checkbox_uncheck_alert)
        select_category_layout.addLayout(button_layout)
        for category in self.categorized_posts.keys():
            if self.categorized_posts[category]:
                checkbox = QCheckBox(category)
                select_category_layout.addWidget(checkbox)
                self.category_check.append(checkbox)

        self.select_category.setLayout(select_category_layout)

        self.set_interval_label = QLabel('시간 간격')
        self.set_interval = QComboBox(self)
        self.set_interval.addItems(['일별', '주별', '월별', '연도별'])
        self.set_interval.currentIndexChanged.connect(self._set_interval)
        self.interval = slice(10)

        set_interval_layout = QHBoxLayout()
        set_interval_layout.addWidget(self.set_interval_label)
        set_interval_layout.addWidget(self.set_interval)

        graph_detail = QVBoxLayout()
        graph_detail.addWidget(self.select_category)
        graph_detail.addLayout(set_interval_layout)

        set_graph_detail = QGroupBox('그래프 세부사항')
        set_graph_detail.setLayout(graph_detail)

        make_graph = QPushButton('그래프 생성', self)
        make_graph.clicked.connect(self.draw_graph)

        self.graph = None
        self.graph_type = 'line'

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()

        graph_setting = QVBoxLayout()
        graph_setting.addWidget(select_graph_type)
        graph_setting.addWidget(set_graph_detail)
        graph_setting.addStretch()
        graph_setting.addWidget(self.progress_bar)
        graph_setting.addWidget(make_graph)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(graph_setting)
        self.setLayout(self.main_layout)
        self.main_layout.setStretchFactor(graph_setting, 0)

        self.setWindowTitle("자료 시각화")
        self.resize(150, 600)
        self.center()

    def show_line_widget(self):
        self.graph_type = 'line'
        for checkbox in self.category_check:
            checkbox.setChecked(False)
        self.select_category.show()
        self.set_interval_label.show()
        self.set_interval.show()

    def show_bar_widget(self):
        self.graph_type = 'bar'
        for checkbox in self.category_check:
            checkbox.setChecked(False)
        self.select_category.show()
        self.set_interval_label.hide()
        self.set_interval.hide()

    def show_pie_widget(self):
        self.graph_type = 'pie'
        self.select_category.hide()
        self.set_interval_label.hide()
        self.set_interval.hide()

    def _set_interval(self, idx: int):
        if idx == 0:
            self.interval = slice(10)
        elif idx == 1:
            self.interval = 'week'
        elif idx == 2:
            self.interval = slice(0, 7)
        else:
            self.interval = slice(0, 4)

    def check_all_category(self):
        for checkbox in self.category_check:
            checkbox.setChecked(True)

    def uncheck_all_category(self):
        for checkbox in self.category_check:
            checkbox.setChecked(False)

    def draw_graph(self):
        self.progress_bar.show()
        if self.graph:
            self.main_layout.removeWidget(self.graph)

        if self.graph_type == 'line':
            x = []
            y = {}

            if self.interval == 'week':
                for post in sorted(self.posts, key=lambda contents: contents.date):
                    year, month, day = map(int, post.date[:10].split('.'))
                    week = datetime.datetime(year, month, day).strftime('%Y.%U')
                    if week not in x:
                        x.append(week)
                for checkbox in self.category_check:
                    if checkbox.isChecked():
                        y[checkbox.text()] = [0] * len(x)
                for category, posts in self.categorized_posts.items():
                    if category in y.keys():
                        for post in posts:
                            year, month, day = map(int, post.date[:10].split('.'))
                            week = datetime.datetime(year, month, day).strftime('%Y.%U')
                            y[category][x.index(week)] += 1
            else:
                for post in sorted(self.posts, key=lambda contents: contents.date[self.interval]):
                    if post.date[self.interval] not in x:
                        x.append(post.date[self.interval])
                for checkbox in self.category_check:
                    if checkbox.isChecked():
                        y[checkbox.text()] = [0] * len(x)
                for category, posts in self.categorized_posts.items():
                    if category in y.keys():
                        for post in posts:
                            y[category][x.index(post.date[self.interval])] += 1

            if y:
                self.graph = line_graph('날짜별 게시물 증가 추이', x, y, '게시 일자', '게시물 수')
                self.checkbox_uncheck_alert.hide()
            else:
                self.checkbox_uncheck_alert.show()
        elif self.graph_type == 'bar':
            x = []
            y = {'게시물': []}
            for checkbox in self.category_check:
                if checkbox.isChecked():
                    x.append(checkbox.text())
                    y['게시물'].append(len(self.categorized_posts[checkbox.text()]))
            if y['게시물']:
                self.graph = bar_graph('주제별 게시물 수', x, y, '주제', '게시물 수')
                self.checkbox_uncheck_alert.hide()
            else:
                self.checkbox_uncheck_alert.show()
        else:
            ratio = {}
            for category in self.categorized_posts.keys():
                post_num = len(self.categorized_posts[category])
                if post_num != 0:
                    ratio[category] = post_num
            self.graph = pie_graph('주제별 게시물 비율', ratio)

        if self.graph:
            self.main_layout.insertWidget(0, self.graph)
            self.resize(1000, 600)

        self.progress_bar.hide()
        self.center()


class KeywordEditWindow(QDialog, WindowWithExtraFunctions):
    def __init__(self):
        super().__init__()

        precaution_text = '''*셀을 더블클릭하면 내용을 수정할 수 있습니다.
*키워드는 쉼표(,)로 구분되며,
 쉼표 양 옆에는 띄어쓰기가 없어야 합니다.
*빈 카테고리는 자동으로 삭제됩니다.
*창을 닫기 전에 반드시 저장을 눌러주세요.'''
        precaution = QLabel(precaution_text, self)
        precaution.setObjectName('precaution')
        precaution.setStyleSheet('QLabel#precaution {color: red}')

        file = open('category_keywords.pickle', 'rb')
        category_with_keywords = pickle.load(file)
        file.close()

        self.category_table = QTableWidget(1, 2)
        self.category_table.setHorizontalHeaderLabels(['카테고리', '키워드'])
        self.category_table.setColumnWidth(0, 100)
        self.category_table.setColumnWidth(1, 350)
        self.category_table.setMinimumSize(500, 400)

        self.categories = QComboBox()
        delete_button = QPushButton('카테고리 삭제')
        delete_button.clicked.connect(self.delete_category)

        delete_layout = QHBoxLayout()
        delete_layout.addWidget(self.categories)
        delete_layout.addWidget(delete_button)
        delete_layout.addStretch()

        self.new_category_name = QLineEdit()
        add_button = QPushButton('카테고리 추가')
        add_button.clicked.connect(self.add_category)

        add_layout = QHBoxLayout()
        add_layout.addWidget(self.new_category_name)
        add_layout.addWidget(add_button)
        add_layout.addStretch()

        for category, keywords in category_with_keywords.items():
            self.categories.addItem(category)

            category = QTableWidgetItem(category)
            keywords = QTableWidgetItem(','.join(keywords))

            category.setTextAlignment(Qt.AlignCenter)

            row_cnt = self.category_table.rowCount()
            if row_cnt < len(category_with_keywords):
                self.category_table.insertRow(row_cnt)

            self.category_table.setItem(row_cnt - 1, 0, category)
            self.category_table.setItem(row_cnt - 1, 1, keywords)

        reset_button = QPushButton('초기화 및 종료')
        reset_button.clicked.connect(self.reset)

        save_button = QPushButton('저장')
        save_button.clicked.connect(self.save)

        reset_save_layout = QHBoxLayout()
        reset_save_layout.addWidget(save_button)
        reset_save_layout.addStretch()
        reset_save_layout.addWidget(reset_button)

        edit_layout = QVBoxLayout()
        edit_layout.addLayout(add_layout)
        edit_layout.addLayout(delete_layout)
        edit_layout.addLayout(reset_save_layout)

        edit = QGroupBox('편집')
        edit.setLayout(edit_layout)

        right_side = QVBoxLayout()
        right_side.addWidget(precaution)
        right_side.addWidget(edit)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.category_table)
        main_layout.addStretch()
        main_layout.addLayout(right_side)

        self.setLayout(main_layout)
        self.setWindowTitle('키워드 편집')
        self.resize(800, 400)
        self.center()

    def delete_category(self):
        idx = self.categories.currentIndex()
        reply = QMessageBox.question(self, 'Message', '이 카테고리를 삭제하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.category_table.removeRow(idx)
            self.categories.removeItem(idx)
            QMessageBox.information(self, 'Message', '삭제되었습니다.', QMessageBox.Ok)

    def add_category(self):
        new_category_name = self.new_category_name.text()
        if new_category_name:
            self.categories.addItem(new_category_name)

            new_category_name = QTableWidgetItem(new_category_name)
            new_category_name.setTextAlignment(Qt.AlignCenter)
            row_cnt = self.category_table.rowCount()
            self.category_table.insertRow(row_cnt)
            self.category_table.setItem(row_cnt, 0, new_category_name)

    def reset(self):
        reply = QMessageBox.question(self, 'Message', '초기화하시겠습니까?\n(초기화된 값은 자동으로 저장됩니다.)',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            category_with_keywords = {
                '기숙사': ['기숙사', '사감', '정독', '소학', '요양', '벌점', '자습', '냉장', '점호', '폰', '스탠딩'],
                '급식': ['급식', '영양사', '조리사', '메뉴', '점심', '잔반', '배식'],
                '입시': ['입시', '대학', '면접', '논술', '원서'],
                '음악실': ['음악실', '노래방', '악기', '피아노', '드럼', '바이올린'],
                '신입생': ['신입생', '예비', '입학'],
                '건의사항': ['대나무숲', '페이지', '대숲', '건의사항', '신문고', '규정', '폰'],
                '본관': ['본관', '도서관', '공강', '성적', '미술실', '레이저', '홈룸', '수업', '체육관'],
                '청결': ['쓰레기', '청소', '냄새'],
                '종소리': ['종소리', '벨소리', '기상송', '방송부'],
                '운동장': ['운동장', '축구']
            }
            file = open('category_keywords.pickle', 'wb')
            pickle.dump(category_with_keywords, file)
            file.close()
            self.close()

    def save(self):
        reply = QMessageBox.question(self, 'Message', '저장하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            category_exists = False
            category_with_keywords = {}
            for i in range(self.category_table.rowCount()):
                category = self.category_table.item(i, 0)
                keywords = self.category_table.item(i, 1)
                if category and keywords and category.text() and keywords.text():
                    category = category.text()
                    keywords = keywords.text()
                    category_exists = True
                    category_with_keywords[category] = keywords.split(',')

            if category_exists:
                file = open('category_keywords.pickle', 'wb')
                pickle.dump(category_with_keywords, file)
                file.close()
                QMessageBox.information(self, 'Message', '저장되었습니다.', QMessageBox.Ok)
            else:
                QMessageBox.information(self, 'Message', '1개 이상의 카테고리를 설정해주세요.', QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
