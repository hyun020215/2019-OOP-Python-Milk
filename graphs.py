# 그래프를 그리기 위한 모듈
import matplotlib as mpl
import matplotlib.pyplot as plt


# 그래프 클래스
class Graph:
    # 한글 폰트 설정: 나눔스퀘어레귤러
    font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/NanumSquareR.ttf').get_name()
    mpl.rc('font', family=font_name)

    # 막대그래프 그리기
    # 매개변수 - title: 그래프 제목, x: x축 값(분류 범주), y: y축 값(데이터 리스트 묶음, 최대 10개), x_label: x축 제목, y_label: y축 제목
    @ staticmethod
    def bar_graph(title: str, x: list, y: dict, x_label: str, y_label: str) -> None:
        # 그래프에 값 표시
        values = list(y.items())
        shift = 0.03 * values[0][1][0]
        for i in range(len(values)):
            label, value = values[i]
            rects = plt.bar([j+0.05*(-len(values)+1+2*i) for j in range(len(x))], value, width=0.1, label=label)
            for j, rect in enumerate(rects):
                plt.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height() + shift, str(value[j]), ha='center')

        # 그래프 축 제목, 범례, 제목 등의 요소 표시
        plt.xticks([i for i in range(len(x))], x)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.title(title)

        # 그래프 띄우기
        plt.show()

    # 꺾은선그래프 그리기
    # 매개변수 - title: 그래프 제목, x: x축 값(분류 범주), y: y축 값(데이터 리스트 묶음), x_label: x축 제목, y_label: y축 제목
    @ staticmethod
    def line_graph(title: str, x: list, y: dict, x_label: str, y_label: str) -> None:
        # 그래프에 값 표시
        shift = 0.03 * list(y.items())[0][1][0]
        for label, value in y.items():
            plt.plot(x, value, label=label, marker='o')
            for i in range(len(value)):
                plt.text(x[i], value[i] + shift, str(value[i]), ha='center')

        # 그래프 축 제목, 범례, 제목 등의 요소 표시
        plt.xticks([i+1 for i in range(len(x))], x)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.title(title)

        # 그래프 띄우기
        plt.show()

    # 원그래프 그리기
    # 매개변수 - title: 그래프 제목, data: 데이터 셋 {범주: 값} 묶음
    @ staticmethod
    def pie_graph(title: str, data: dict) -> None:
        # 그래프에 값 표시
        plt.pie(list(data.values()), labels=list(map(lambda x: x + '\n' + str(data[x]), data.keys())),
                startangle=90, shadow=True, explode=[0.1 if i == 0 else 0 for i in range(len(data))], autopct='%1.1f%%')

        # 그래프 제목 표시
        plt.title(title)

        # 그래프 띄우기
        plt.show()


if __name__ == '__main__':
    Graph.bar_graph('막대그래프', [1, 2, 3], {'값1': [2, 3, 4], '값2': [4, 1, 2]}, '가로', '세로')
    Graph.line_graph('꺾은선그래프', [1, 2, 3], {'값1': [3, 4, 5], '값2': [4, 1, 2]}, '가로', '세로')
    Graph.pie_graph('원그래프', {'값1': 124, '값2': 235, '값3': 412})
