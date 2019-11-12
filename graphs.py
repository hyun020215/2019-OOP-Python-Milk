import matplotlib.pyplot as plt


class Graph:
    @ staticmethod
    def bar_graph(title, x, y, x_label, y_label):
        plt.bar(x, y, width=0.3)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

    @ staticmethod
    def line_graph(title, x, y, x_label, y_label):
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()


if __name__ == '__main__':
    Graph.bar_graph(title='practice', x=['dorm', 'cafe', 'suggest'], y=[3, 5, 2], x_label='topic', y_label='number')