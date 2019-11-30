import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 한글 폰트 설정: 나눔스퀘어레귤러
font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/NanumSquareR.ttf').get_name()
mpl.rc('font', family=font_name)


# 막대그래프 그리기
# 매개변수 - title: 그래프 제목, x: x축 값(분류 범주), y: y축 값(데이터 리스트 묶음, 최대 10개), x_label: x축 제목, y_label: y축 제목
def bar_graph(title: str, x: [int or str], y: {str: [int or float]}, x_label: str, y_label: str) -> FigureCanvas:
    # 그래프 준비
    fig = plt.Figure()
    ax = fig.add_subplot(111)

    # 그래프에 값 표시
    values = list(y.items())
    shift = 0.01 * values[0][1][0]
    for i in range(len(values)):
        label, value = values[i]
        rects = ax.bar([j+0.05*(-len(values)+1+2*i) for j in range(len(x))], value, width=0.1, label=label)
        for j, rect in enumerate(rects):
            ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height() + shift, str(value[j]), ha='center')

    # 그래프 축 제목, 범례, 제목 등의 요소 표시
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    ax.set_title(title)

    # 캔버스에 그래프 띄우기
    canvas = FigureCanvas(fig)
    canvas.draw()
    canvas.show()

    return canvas


# 꺾은선그래프 그리기
# 매개변수 - title: 그래프 제목, x: x축 값(분류 범주), y: y축 값(데이터 리스트 묶음), x_label: x축 제목, y_label: y축 제목
def line_graph(title: str, x: [int or float], y: {str: [int or float]}, x_label: str, y_label: str) -> FigureCanvas:
    # 그래프 준비
    fig = plt.Figure()
    ax = fig.add_subplot(111)

    # 그래프에 값 표시
    shift = 0.01 * list(y.items())[0][1][0]
    for label, value in y.items():
        ax.plot(x, value, label=label, marker='o')
        for i in range(len(value)):
            ax.text(x[i], value[i] + shift, str(value[i]), ha='center')

    # 그래프 축 제목, 범례, 제목 등의 요소 표시
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    ax.set_title(title)

    # 캔버스에 그래프 띄우기
    canvas = FigureCanvas(fig)
    canvas.draw()
    canvas.show()

    return canvas


# 원그래프 그리기
# 매개변수 - title: 그래프 제목, data: 데이터 셋 {범주: 값} 묶음
def pie_graph(title: str, data: {str: int or float}) -> FigureCanvas:
    fig = plt.Figure()
    ax = fig.add_subplot(111)

    # 그래프에 값 표시
    ax.pie(list(data.values()), labels=list(map(lambda x: x + '\n' + str(data[x]), data.keys())), startangle=90,
           shadow=True, explode=[0.1 if i == 0 else 0 for i in range(len(data))], autopct='%1.1f%%')

    # 그래프 제목 표시
    ax.set_title(title)

    # 캔버스에 그래프 띄우기
    canvas = FigureCanvas(fig)
    canvas.draw()
    canvas.show()

    return canvas
