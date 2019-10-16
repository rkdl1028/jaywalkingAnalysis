# column 두개 받아서 그래프 그리고(png파일), 이미지파일을 객체에 저장
# 해당 객체를 임의로 이름 지정 후 String으로 변환> String io  ../static/images 경로 지정하여 저장
# 두개 입력 받았을때만 제출 되도록 예외처리

import random
import tempfile

# 파일이름을 임의로 지정하기 위해 random list 생성
def random_list():
    list=[]
    count=0
    while True:
        list.append(count)
        count=count+1
        if len(list)==5:
            break
    return list
from io import StringIO

from PIL import Image
image_file = StringIO(open("test.jpg",'rb').read())
im = Image.open(image_file)
