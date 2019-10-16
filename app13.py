# flask 모듈 임포트
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import json
import folium
import xlrd
import base64
import io
import db
import read_data
import Base64_encoding
import urllib


# flask 객체 생성
app = Flask(__name__)

anal_data = db.data_translate_dataframe() # 디비 데이터를 df로 변환하여 가져온다.
whole=read_data.plus_wi_gyung(anal_data) # 해당 디비 데이터에 위도 경도를 추가해놓는거


# 라우터 등록 => 웹상 루트 주소 생성
@app.route('/kssj')
def kssj():
    return render_template('kssj.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/page1')
def page1():
    accident = whole.loc[:, ['자치구', '무단횡단 사고']].copy()
    rank = []
    rank.append(accident["자치구"].tolist())
    rank.append(accident["무단횡단 사고"].tolist())
    return render_template('page1.html', rank=rank, menu = 'page1')

@app.route('/page1/iframe')
def page1_frame():
    whole[['위도']] = whole[['위도']].apply(pd.to_numeric)
    whole[['경도']] = whole[['경도']].apply(pd.to_numeric)

    geo_path = 'dynamic/data/02. skorea_municipalities_geo_simple.json'

    geo_str = json.load(open(geo_path, encoding='utf-8'))
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
    folium.Choropleth(geo_data=geo_str,
                      data=whole,
                      columns=['자치구', '무단횡단 사고'],
                      fill_color='PuRd',
                      key_on='feature.id').add_to(map)
    for n in whole.index:
        folium.CircleMarker([whole['위도'][n], whole['경도'][n]],
                            popup=folium.Popup(
                                '<a href="http://18.216.41.70/page2?gu=%s" target="_top">' %(whole['자치구'][n]) + whole['자치구'][n] + '</a>',
                                max_width=300,
                                show=True,),
                            radius=0.1 ).add_to(map)
    return map._repr_html_()



@app.route('/page2',methods=['GET'])
def page2():

    gu=request.args['gu']


    return render_template('page2.html',gu=gu,menu = 'page2')

@app.route('/page3', methods=['GET'])
@app.route('/page3/<c1>&<c2>', methods=['GET'])
def page3(): # 자치구 뺀 전처리
    col_list = []
    for string in anal_data.columns:
        col_list.append(string)
    col_list.remove('자치구')
    # page3.html 파일에서 form 태그를 통해 columns1,columns2를 전달받음 (칼럼)
    c1 = request.args['c1']
    c2 = request.args['c2']
    # Base64_encidng.py에서 해당함수 불러와 인코딩 / 디코딩하고 graph_url 반환하여 저장
    graph_url=Base64_encoding.build_graph(c1, c2)
    return render_template('page3.html',menu = 'page3',list=col_list,graph_url = graph_url,c1=c1,c2=c2)

@app.route('/page5/iframe',methods=['GET'])
@app.route('/page5/iframe/<gugu>',methods=['GET'])
def page5_iframe(gugu=None):
    gu2 = str(gugu)
    json1 = 'http://taas.koroad.or.kr/data/rest/frequentzone/pdestrians/jaywalking?authKey=Ba00L%2B7Jna%2BKXC4%2B29ePOemMfI9i%2BdtCJZ%2B8HUf32aHH847OLCuA4PSRPCOR2DgZ&searchYearCd=2018045&sido=11&guGun='+gu2+'&type=json'
    print(json1)
    request = urllib.request.Request(json1)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        fir_dict = json.loads(response_body.decode('utf-8'))
        sec_dict = fir_dict.get('items')
        items = []
        for i in sec_dict:
            items += sec_dict[i]
        spot_name = []
        lo = []
        la = []
        leng = len(items)
        for item in items:
            for key in item.keys():
                if key == 'spot_nm':
                    spot_name.append(item[key])
        for item in items:
            for key in item.keys():
                if key == 'lo_crd':
                    lo.append(float(item[key]))
        for item in items:
            for key in item.keys():
                if key == 'la_crd':
                    la.append(float(item[key]))
    sp_nm = []
    for k in range(len(spot_name)):
        a = spot_name[k].split(' ')
        sp_nm.append(' '.join(a[2:]))
    map = folium.Map(location=[la[0], lo[0]], zoom_start=14)
    for i in range(leng):
        folium.CircleMarker([la[i], lo[i]],
                            popup=folium.Popup(sp_nm[i],
                                               max_width=300,
                                               show=True, ),
                            radius=0.1).add_to(map)
    return map._repr_html_()

@app.route('/page5',methods=['GET'])
def page5():
    gu1 = request.args.get('gugu')
    if gu1 == None:
        gu1 = '260'
    return render_template('page5.html',gu1=gu1, menu = 'page5')



# 앱 실행  --> 마지막 위치 유지
# 웹주소와 포트 지정
app.run(host='0.0.0.0',port="80",debug=True)

