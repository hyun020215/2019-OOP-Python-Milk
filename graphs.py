# 그래프를 그리기 위한 모듈
import matplotlib as mpl
import matplotlib.pyplot as plt


# 그래프 클래스: 막대그래프, 꺾은선그래프 등 다양한 그래프를 그릴 수 있다.
class Graph:
    # 막대그래프 그리기
    # 매개변수 - title: 그래프 제목, x: x축 값(분류 범주), y: y축 값(데이터 리스트 묶음, 최대 10개), x_label: x축 제목, y_label: y축 제목
    @ staticmethod
    def bar_graph(title: str, x: list, y: dict, x_label: str, y_label: str) -> None:
        # 한글 폰트 설정: 나눔스퀘어레귤러
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/NanumSquareR.ttf').get_name()
        mpl.rc('font', family=font_name)

        # 그래프에 값 표시
        values = list(y.items())
        for i in range(len(values)):
            label, value = values[i]
            plt.bar([j+0.05*(-len(values)+1+2*i) for j in range(len(x))], value, width=0.1, label=label)

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
        # 한글 폰트 설정: 나눔스퀘어레귤러
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/NanumSquareR.ttf').get_name()
        mpl.rc('font', family=font_name)

        # 그래프에 값 표시
        for label, value in y.items():
            plt.plot(x, value, label=label, marker='o')

        # 그래프 축 제목, 범례, 제목 등의 요소 표시
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
        # 한글 폰트 설정: 나눔스퀘어레귤러
        font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/NanumSquareR.ttf').get_name()
        mpl.rc('font', family=font_name)

        # 그래프에 값 표시
        plt.pie(list(data.values()), labels=list(data.keys()), startangle=90, shadow=True, autopct='%1.1f%%')

        # 그래프 제목 표시
        plt.title(title)

        # 그래프 띄우기
        plt.show()


if __name__ == '__main__':
    Graph.pie_graph(title='국가별 기여도', data={'Korea': 124, 'Japan': 235, 'America': 412})
