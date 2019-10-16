# 그림파일 웹에 뿌려주기 위해 인코딩 과정
import io
import base64
import db
import seaborn as sns
# Matplotlib 한글처리
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 사전형식으로 데이터프레임 생성되고, 실제 데이터 들어있음


# 우분투에서 돌아가므로 우분투경로로 잡아줌
path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
fontprop = fm.FontProperties(fname=path, size=12)

# base64 그림파일 인코딩 / 디코딩
def build_graph(x_columns, y_columns):
    anal_data = db.data_translate_dataframe()
    img = io.BytesIO()  # img 객체를 바이트버퍼에 생성

    # 그래프 표현부분
    # 아예 그래프 전체 다 그려서 반환하는 함수 구현해보기!!!!!!
    sns.regplot(anal_data[x_columns],anal_data[y_columns])
    cor=anal_data[x_columns].corr(anal_data[y_columns]) # 상관계수
    cor=round(cor,3) # 소수점 반올림
    plt.title(cor)
    plt.xlabel(x_columns,fontproperties=fontprop)
    plt.ylabel(y_columns,fontproperties=fontprop)
    plt.grid()

    plt.savefig(img, format='png')  # 그린것 버퍼에 저장됨
    img.seek(0)  # 바이트 0번째로 이동
    graph_url = base64.b64encode(img.getvalue()).decode()  # 해당 변수에는 바이트값 img가 디코딩 된 것이 저장(그림파일 실제 저장된 주소)
    plt.close() # 표현해주고 삭제
    return 'data:image/png;base64,{}'.format(graph_url)