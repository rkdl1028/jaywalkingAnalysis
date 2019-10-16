import pandas as pd
import seaborn as sns
import db
from sklearn import preprocessing # 머신러닝 전처리 => 데이터 정규화
import matplotlib.pyplot as plt

# 분석 끝나서 동적으로 쓸때 데이터프레임 db로 부터 받아올 필요있음.
# 전처리전 db 연결해서 데이터 뽑아옴
conn=db.get_connection()
anal_list_table=db.get_anal_list(conn)


# matplotlib 한글 폰트 처리
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus']=False

if platform.system()=='Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name=font_manager.FontProperties(fname=path).get_name()
    rc('font',family=font_name)

ac_anal=pd.read_excel('dynamic/data/ac_anal.xls',encoding='euc-kr')
pop_seoul=pd.read_excel('dynamic/data/Pop_seoul_real.xls',encoding='euc-kr')
ac_anal=pd.merge(ac_anal,pop_seoul,on='자치구')
ac_anal.set_index('자치구',inplace=True)

ac_anal['미성년자']=ac_anal['5~9세']+ac_anal['10~14세']+ac_anal['15~19세']
del ac_anal['10~14세']
del ac_anal['5~9세']
del ac_anal['15~19세']

# 상관관계 및 정규화 대상 칼럼 지정
col1 = ['무단횡단 사고',
        '중국인',
        '유흥업소']

col2 = ['무단횡단 사고',
        '유기동물보호현황',
        '인구밀도',
        '통근,통학',
        '총인구합계']

col3 = ['무단횡단 사고',
        '도로 총 계',
        '광로(40m이상)', '대로(25~40)', '중로(12~25)', '소로(12m미만)']

col4 = ['무단횡단 사고', '횡단보도수', '신호등O', '신호등X']

col5 = ['무단횡단 사고',
        '기초생활수급자',
        '미성년자', '노인인구합계']

col_list = [col1, col2, col3, col4, col5]


# 정규화 모듈

def Normalize(column_list):
    x = ac_anal[column_list].values
    min_max_scaler = preprocessing.MinMaxScaler()  # 전처리 모듈
    x_scaled = min_max_scaler.fit_transform(x.astype(float))

    ac_anal_norm = pd.DataFrame(x_scaled, columns=column_list, index=ac_anal.index)  # 정규화 DataFrame 생성

    return ac_anal_norm
# col1 ~ col5에 대한 정규화 테이블 생성

ac_anal_norm1=Normalize(col1) # 무단횡단 / 중국인 / 유흥업소
ac_anal_norm2=Normalize(col2) # '무단횡단 사고','유기동물보호현황','인구밀도','통근,통학'
ac_anal_norm3=Normalize(col3) # '무단횡단 사고','도로 총 계','광로(40m이상)','대로(25~40)','중로(12~25)','소로(12m미만)','도로연장당 횡단보도 수'
ac_anal_norm4=Normalize(col4) # '무단횡단 사고','횡단보도수','신호등O','신호등X'
ac_anal_norm5=Normalize(col5) # '무단횡단 사고','기초생활수급자','5~9세','10~14세','15~19세','노년부양비','노령화지수'

# 사진 저장 경로 수정해야함
# 그래프 사진 저장
# 영등포구 >> 무단횡단사고/중국인/유흥업소 수 히트맵
plt.figure(figsize = (15, 16))
Y_plot1=sns.heatmap(data = ac_anal_norm1, annot = True, fmt = '.2f', cmap = 'Reds')
fig1=Y_plot1.get_figure()
#fig1.savefig('C:\Multicampus_kssj\Anal_image\Yongdeungpo1_hitmap.png')
fig1.savefig('C:\Last_kssj_project\static')
# 영등포구 >> 무단횡단사고/중국인/유흥업소 상관계수 히트맵
plt.figure(figsize = (10, 10))
Y_plot2=sns.heatmap(data = ac_anal_norm1.corr(), annot = True, fmt = '.2f', cmap = 'Reds')
fig2=Y_plot2.get_figure()
fig2.savefig('C:\Multicampus_kssj\Anal_image\Yondeungpo2_corr_hitmap.png')

# 영등포구 >> 무단횡단사고/중국인/유흥업소 상관관계 pairplot
Y_plot3=sns.pairplot(ac_anal_norm1,x_vars=['중국인','유흥업소'],y_vars=['무단횡단 사고'],kind='reg',size=5)
Y_plot3.savefig('C:\Multicampus_kssj\Anal_image\Yondeungpo3_corr_pairplot.png')

# ***********************************************

# 2.관악구
plt.figure(figsize = (15, 15))
G_plot1=sns.heatmap(data = ac_anal_norm2, annot = True, fmt = '.2f', cmap = 'Blues')
fig1=G_plot1.get_figure()
fig1.savefig('C:\Multicampus_kssj\Anal_image\Gwanak1_hitmap.png')

plt.figure(figsize = (10, 10))
G_plot2=sns.heatmap(data = ac_anal_norm2.corr(), annot = True, fmt = '.2f', cmap = 'Blues')
fig2=G_plot2.get_figure()
fig2.savefig('C:\Multicampus_kssj\Anal_image\Gwanak2_corr_hitmap.png')

G_plot3=sns.pairplot(ac_anal_norm2,vars=['무단횡단 사고','인구밀도','통근,통학'],kind='reg',size=3)
G_plot3.savefig('C:\Multicampus_kssj\Anal_image\Gwanak3_corr_pairplot.png')

# 3.종로구
plt.figure(figsize = (15, 15))
J_plot1=sns.heatmap(data = ac_anal_norm5, annot = True, fmt = '.2f', cmap = 'Blues')
fig1=J_plot1.get_figure()
fig1.savefig('C:\Multicampus_kssj\Anal_image\Jongro1_hitmap.png')

plt.figure(figsize = (10, 10))
J_plot2=sns.heatmap(data = ac_anal_norm5.corr(), annot = True, fmt = '.2f', cmap = 'Blues')
fig2=J_plot2.get_figure()
fig2.savefig('C:\Multicampus_kssj\Anal_image\Jongro2_corr_hitmap.png')

J_plot3=sns.pairplot(ac_anal_norm3,x_vars=['광로(40m이상)','대로(25~40)','중로(12~25)','소로(12m미만)'],y_vars=['무단횡단 사고'],kind='reg',size=5)
J_plot3.savefig('C:\Multicampus_kssj\Anal_image\Jongro3_corr_pairplot.png')