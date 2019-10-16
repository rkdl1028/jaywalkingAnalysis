import db
import pandas as pd


# 분석 데이터 불러와야함

anal_merge=db.data_translate_dataframe()


def plus_wi_gyung(anal_merge):
    # anal_merge=db.data_translate_dataframe() #anal merge를 db에 불러온다.
    wi_gyung=pd.read_excel('dynamic/data/전체현황_위경도추가.xls', encoding='euc-kr') #위도경도데이터 들어있는 데이터프레임
    wi_gyung=wi_gyung.loc[:,['자치구','위도','경도']]
    sum_data=pd.merge(anal_merge,wi_gyung,on='자치구')

    return sum_data




