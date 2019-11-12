import matplotlib as mpl
import matplotlib.pyplot as plt


class Graph:
    @ staticmethod
    def bar_graph(title, x, y, x_label, y_label):
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
        mpl.rc('font', family=font_name)

        plt.bar(x, y, width=0.3)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

    @ staticmethod
    def line_graph(title, x, y, x_label, y_label):
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
        mpl.rc('font', family=font_name)

        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()


if __name__ == '__main__':
    Graph.bar_graph(title='주제별 게시물 건수', x=['기숙사', '급식', '건의사항'], y=[3, 5, 2], x_label='주제', y_label='건수')