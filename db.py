# AWS DB 접속
import pymysql
import pandas as pd

# 데이터베이스 접속
def get_connection():
    conn = pymysql.connect(host='database-1.cxs7lnlzes7w.us-east-2.rds.amazonaws.com',user='root',password='12341234',db='anal_data',charset='utf8')
    return conn

# AWS mysql로부터 데이터받아와 Dict자료형으로 바꿈
def get_anal_list():
    conn=get_connection()

    # mysql로부터 데이터 가져올때 Dict자료형으로 가져옴(칼럼명 유지 위해)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # 쿼리
    sql='select * from sum_anal'
    cursor.execute(sql)
    anal_list=cursor.fetchall()
    conn.close()

    return anal_list

# 프로그램에서 가용할 수 있도록 Datafame으로 변환(Dict)
def data_translate_dataframe():
    # conn = get_connection() # db연결정보 conn에 저장
    anal_list_table = get_anal_list() # dict 자료형으로 불러와 저장
    anal_list_table = pd.DataFrame(anal_list_table) # 데이터프레임 변환

    return anal_list_table
