'''import pymysql
import pandas as pd
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()

anal_merge=pd.read_csv('dynamic/data/anal_merge.csv')
engine = create_engine("mysql+mysqldb://", encoding='utf-8')
conn=engine.connect()

anal_merge.to_sql(name='sum_anal', con=engine, if_exists='append',index=False)

conn.close()'''

# anal_data_result로 타겟 되어있음
# 터미널 통해서 실행할것 (python app11.py)

# Data파일을 mysql db에 삽입 (한번만 실행할것)
import pymysql
import pandas as pd
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()

# aws db 연결하고 스키마삽입과 동시에 anal_merge.csv 데이터 테이블 삽입
anal_merge=pd.read_csv('anal_merge.csv')
anal_merge['미성년자']=anal_merge['5~9세']+anal_merge['10~14세']+anal_merge['15~19세']
del anal_merge['5~9세']
del anal_merge['10~14세']
del anal_merge['15~19세']

#innodb스키마에 접속
engine = create_engine("mysql+mysqldb://root:"+"12341234"+"@database-1.c2z9tseum4tk.us-east-2.rds.amazonaws.com/innodb", encoding='utf-8')
conn=engine.connect()

# anal_merge를 테이블로 삽입
anal_merge.to_sql(name='anal_data_result', con=engine, if_exists='append',index=False)

conn.close()
