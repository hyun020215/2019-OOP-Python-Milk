import matplotlib as mpl
import matplotlib.pyplot as  plt


class Graph:
    @ staticmethod
    def bar_graph(title: str, x: list, y: dict, x_label: str, y_label: str) -> None:
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
        mpl.rc('font', family=font_name)

        values = list(y.items())
        for i in range(len(values)):
            label, value = values[i]
            plt.bar([j+0.1*(-len(values)+1+2*i) for j in range(len(x))], value, width=0.2, label=label)
        plt.xticks([i for i in range(len(x))], x)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.title(title)
        plt.show()

    @ staticmethod
    def line_graph(title: str, x: list, y: dict, x_label: str, y_label: str) -> None:
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
        mpl.rc('font', family=font_name)

        for label, value in y.items():
            plt.plot(x, value, label=label, marker='o')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.title(title)
        plt.show()


if __name__ == '__main__':
    Graph.bar_graph(title='주제별 게시물 건수', x=['기숙사', '급식', '건의사항'], y={'post': [3, 5, 2], 'what': [1, 2, 3], 'who': [3, 2, 1]}, x_label='주제', y_label='건수')
