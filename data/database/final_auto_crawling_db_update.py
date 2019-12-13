#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import requests
import json

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta


import time
from konlpy.corpus import kolaw
from konlpy.tag import Kkma
import nltk
import konlpy

import pickle
import joblib


# # 축제 정보 크롤링 자동화

# ## 기간지정

# In[2]:


start_date = '{}'.format(datetime.now().strftime("%Y%m%d"))
end_date = '{}'.format((datetime.now()+ timedelta(days=30)).strftime("%Y%m%d"))


# In[3]:


driver = webdriver.Chrome('C:/Users/MINJI/chromedriver')
search_period = [start_date, end_date]
page_num = 1

driver.get('https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pMenuCD=&pCurrentPage={}&pSearchType=01&pSearchWord=&pSeq=&pSido=01&pOrder=01down&pPeriod=&fromDt={}&toDt={}search_period'.format(page_num, search_period[0], search_period[1]))
tmp = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/span')
p = re.compile('총 [\d]+건').match(tmp.text).group()
total_festival_num = int(re.findall('\d+', p )[0])

if total_festival_num%5 == 0: 
    last_page_num = int(total_festival_num/5)
else:
    last_page_num = int(total_festival_num/5)+1
    

res = []  
for page_num in range(1, last_page_num+1):
    #print(page_num)
    driver.get('https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pMenuCD=&pCurrentPage={}&pSearchType=01&pSearchWord=&pSeq=&pSido=01&pOrder=01down&pPeriod=&fromDt={}&toDt={}search_period'.format(page_num, search_period[0], search_period[1]))

    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, 'html.parser')

    bb = soup2.find_all('p', attrs={'class':'title'})

    for i in range(1, len(bb)+1):
        
        tmp = driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul/li[{}]/a'.format(i))

        tmp.click()

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'html.parser')

        if soup2.find('p', attrs={'class':'errorInfo'}):
            continue
        else:
            festival_info = dict()

            festival_name = soup2.find('div', attrs={'class': 'view_title color04'}).text
            festival_img = soup2.find('div', attrs={'class': 'culture_view_img'}).find('img')

            festival_info['title'] = festival_name
            festival_info['img'] = festival_img

            for dt, dd in zip(soup2.find_all('dt'), soup2.find_all('dd')):
                festival_info[dt.text] = dd.text.strip()

            festival_info['explanation'] = soup2.find('div', attrs={'class': 'view_con color04'}).text

            res.append(festival_info)

        driver.get('https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pMenuCD=&pCurrentPage={}&pSearchType=01&pSearchWord=&pSeq=&pSido=01&pOrder=01down&pPeriod=&fromDt={}&toDt={}search_period'.format(page_num, search_period[0], search_period[1]))
    page_num += 1


# In[4]:


festival_new = pd.DataFrame(res)


# ## 축제장소 수정

# In[5]:


festival_new['축제장소_수정'] = festival_new['축제장소'].str.split(',', expand=True).iloc[:, 0]


# ### 축제 장소가 NA면 '없음'으로 표시

# In[6]:


festival_new['축제장소_수정'] = np.where(festival_new['축제장소_수정'].isnull(), '없음', festival_new['축제장소_수정'])


# In[7]:


festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('코엑스'), '코엑스', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('Coex'), '코엑스', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('예술의'), '예술의 전당',festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('혜화'), '혜화역', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('한성대입구'), '한성대입구역', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('홍문관'), '홍익대학교 홍문관', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('남산'),  '남산골한옥마을', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('주차장'),  '홍익대학교', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('압구정'),  '압구정로데오역', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('대학로예술극장'),  '대학로예술극장', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('여의도 물빛무대'),  '여의도 물빛무대', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('국립한글박물관'),  '국립한글박물관', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('정동'),  '서울시 중구 정동길', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('서울시청'),  '서울시청광장', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('능동로'),  '서울 능동로', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('청계광장'),  '청계광장', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('강동구청'),  '강동구청', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('서울산업진흥원'), '서울산업진흥원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('서울광장'), '서울시청광장', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('정동'), '서울 중구 정동길', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('KBS'), 'KBS홀', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('홍대 롤링홀'), '홍대 롤링홀', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('학여울역 SETEC 제2/3 전시실'), 'SETEC', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('4대궁 및 종묘'), '창덕궁', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('대학로'), '대학로예술극장', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('여의도 한강공원 일대'), '여의도 한강공원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('고척돔'), '고척스카이돔', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('강서구 개화산'), '강서구 개화산', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('국립한글박물관'),  '국립한글박물관', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('인왕산 청운공원'), '인왕산 청운공원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('세빛섬'), '세빛섬', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('응봉산 팔각정'), '응봉산 팔각정', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('아차산 해맞이'), '아차산 해맞이명소', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('하늘공원'), '하늘공원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('무역센터'), '코엑스', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('W스테이지'), '서울 종로구 북촌로12길 24-5 ', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('뚝섬'), '뚝섬한강공원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('연세로'), '신촌 연세로', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('호국보훈'), '상암 MBC', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('동대문디자인플라자'), '동대문디자인플라자', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('국회'), '국회의사당', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('현대백화점 목동점'), '현대백화점 목동점', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('월드컵공원'), '상암월드컵공원 평화광장', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('서래섬'), '서래섬', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('11개 한강공원'), '여의도 한강공원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('국립4.19민주묘지'), '국립4.19민주묘지', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('최순우옛집'), '최순우옛집', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('올림픽공원'), '올림픽공원', festival_new['축제장소_수정'])
festival_new['축제장소_수정'] = np.where(festival_new['축제장소'].str.contains('국립한글박물관'), '국립한글박물관', festival_new['축제장소_수정'])


# In[8]:


url = "https://dapi.kakao.com/v2/local/search/keyword.json"
apikey = "7f6745340f5774fddc3560cf93bf54b3" 

result = list()
no_info_festival = list()

for nm, location in zip(festival_new['title'], festival_new['축제장소_수정']):
    query = location #검색을 원하는 질의어 : 축제 장소

    r = requests.get( url, params = {'query':query, 'page':45, 'radius':200}, headers={'Authorization' : 'KakaoAK ' + apikey } ) 
    #결과를 json 형식으로 반환
    data = json.loads(r.text)
    #print('축제명: {} \t\t 장소: {}'.format(nm, location))
    if data['meta']['total_count']!=0:        
        for i in data['documents']:
            address_name      = i['address_name']
            place_name        = i['place_name']
            place_url         = i['place_url']
            road_address_name = i['road_address_name']
            x                 = i['x']
            y                 = i['y']

            result.append({
                '축제명'            : nm,
                '축제장소'          : location,
                'address_name'      : address_name,
                'place_name'        : place_name,
                'place_url'         : place_url,
                'road_address_name' : road_address_name,
                'x'                 : x,
                'y'                 : y
            })
    else:
        result.append({
            '축제명'            : nm,
            '축제장소'          : location,
            'address_name'      : None,
            'place_name'        : None,
            'place_url'         : None,
            'road_address_name' : None,
            'x'                 : None,
            'y'                 : None
        })
        no_info_festival.append((nm, location))


# In[9]:


festival_info_new = pd.DataFrame(result, columns = ['축제명', '축제장소','address_name', 'x', 'y', 'road_address_name', 'place_url'])
location_new = festival_info_new.loc[festival_info_new['축제장소']!='없음'].drop_duplicates('축제장소')


# ## 그 외 축제정보와 결합

# In[10]:


festival_new = festival_new.rename(columns={'title':'축제명', '관련 누리집':'관련_누리집', '주최/주관기관':'주최_주관기관', 'explanation':'축제설명'})


# In[11]:


festival_new = pd.merge(festival_new[['축제명', 'img', '개최지역', '개최기간', '축제성격', '관련_누리집', '축제장소', '요금', '소요시간',
       '연령제한', '주최_주관기관', '문의', '축제설명']], location_new[['축제명', 'address_name', 'x', 'y', 'road_address_name',
       'place_url']], on='축제명', how='left')


# # DB에 업데이트

# In[12]:


db_path = "SEOUL_FESTIVAL.db"
table_nm = "FESTIVAL_INFO"
con = sqlite3.connect(db_path, timeout=100)


# In[13]:


cur = con.cursor()
cur.execute('PRAGMA table_info({})'.format(table_nm))
table_columns = [i[1] for i in cur]

add_table = pd.DataFrame(np.zeros(len(table_columns))).T
add_table.columns = table_columns


# In[14]:


cur = con.cursor()
cur.execute('SELECT festival_id, 축제명 FROM {}'.format(table_nm))
origin_festival_id = [i[0] for i in cur]
cur.close()

cur = con.cursor()
cur.execute('SELECT festival_id, 축제명 FROM {}'.format(table_nm))
origin_festival_nm = [i[1] for i in cur]
cur.close()


# In[15]:


# 기존 DB에 없는 축제만 추출
festival_new_2 = festival_new.loc[~festival_new['축제명'].isin(origin_festival_nm)].reset_index(drop=True)

new_festival_id = pd.DataFrame({'festival_id':np.arange(origin_festival_id[-1]+1, origin_festival_id[-1]+1+festival_new_2.shape[0])})
new_values = pd.concat([new_festival_id, festival_new_2], 1)
add_new_table = pd.concat([add_table, new_values], sort = False).iloc[1:]

add_new_table['festival_id'] = add_new_table['festival_id'].astype(int)
add_new_table['img'] = add_new_table['img'].astype(str)

for i in range(add_new_table.shape[0]):
    cur = con.cursor()
    cur.execute("INSERT INTO {} Values {};".format(table_nm, str(tuple(add_new_table.iloc[i].values)).replace('nan', 'NULL').replace('None', 'NULL')))
    cur.close()

con.commit()
con.close()


# # DB에 음식점 추가

# In[16]:


# 음식점 정보 가져오기(카카오)

# import sqlite3, requests
from collections import OrderedDict

def create_restaurants(c):
    c.execute("DROP TABLE IF EXISTS RESTAURANT_INFO")
    c.execute('''CREATE TABLE "RESTAURANT_INFO" (
            "id" INTEGER PRIMARY KEY,
            "place_name" TEXT,
            "category_name" TEXT,
            "category_group_code" TEXT,
            "category_group_name" TEXT,
            "phone" TEXT,
            "address_name" TEXT,
            "road_address_name" TEXT,
            "x" REAL,
            "y" REAL,
            "place_url" TEXT
    );''')

def create_festival_restaurants(c):
    c.execute("DROP TABLE IF EXISTS FESTIVAL_RESTAURANT")
    c.execute('''CREATE TABLE FESTIVAL_RESTAURANT (
        festival_id INTEGER,
        restaurants_id INTEGER,
        distance INTEGER,
        FOREIGN KEY(festival_id) REFERENCES FESTIVAL_INFO(festival_id) ON DELETE SET NULL,
        FOREIGN KEY(restaurants_id) REFERENCES RESTAURANT_INFO(id) ON DELETE SET NULL
    )''')

KEYS = ['id', 'place_name', 'category_name', 'category_group_code',
        'category_group_name', 'phone', 'address_name', 'road_address_name',
        'x', 'y', 'place_url', 'distance']

def get_restaurant(lng, lat, page):
    rsp = requests.get(url,
                       params={"category_group_code": "FD6",
                               'x': str(lng), 'y': str(lat),
                               "radius": 1000, "page": page, "size": 15},
                       headers={"Authorization": "KakaoAK " + apikey}
                       )
    if rsp.status_code != 200:
        raise Exception(rsp.status_code)
    return rsp.json()

def db_session_add(doc, pk, c):
    for d in doc:
        d = OrderedDict((k, d[k]) for k in KEYS)
        t = []
        for k, v in d.items():
            if k != "id" and k != "distance":
                t.append(v)
            elif k == "id":
                t.append(int(v))
                res_id = int(v)
            else:
                dist = int(v)
        c.execute('INSERT INTO FESTIVAL_RESTAURANT VALUES (?,?,?)',
                  (pk, res_id, dist))
        c.execute(
            'INSERT OR IGNORE INTO RESTAURANT_INFO VALUES (?,?,?,?,?,?,?,?,?,?,?)', tuple(t))

def fetch_fes(c):
    """
    in: connection
    out: list
    """
    c.execute("""SELECT festival_id, x, y 
                FROM FESTIVAL_INFO
                WHERE x > 0;""")
    lst = [dict(zip(('id', 'x', 'y'), row)) for row in c]
    return lst


url = "https://dapi.kakao.com/v2/local/search/category.json"

con = sqlite3.connect(db_path)

cur = con.cursor()

create_restaurants(cur)

create_festival_restaurants(cur)

for festival in fetch_fes(cur):
    page = 1
    resp = get_restaurant(festival['x'], festival['y'], page)
    while not resp["meta"]["is_end"]:
        doc = resp["documents"]
        db_session_add(doc, festival['id'], cur)
        page += 1
        resp = get_restaurant(festival['x'], festival['y'], page)
    doc = resp["documents"]
    db_session_add(doc, festival['id'], cur)

con.commit()
con.close()


# # 연령 클러스터 예측

# In[17]:


con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute('SELECT * FROM FESTIVAL_CLUSTER')
cluster_before = pd.DataFrame(cur.fetchall(), columns=['festival_id', '축제명', '클러스터'])
cur.close()


# In[18]:


cur = con.cursor()
cur.execute('SELECT * FROM FESTIVAL_info')
festival_updated = pd.DataFrame(cur.fetchall(), columns=table_columns)
cur.close()
con.close()


# In[19]:


# DB에서 가져오기
target_festival = festival_updated.loc[festival_updated['festival_id'].isin(set(festival_updated['festival_id']) - set(cluster_before['festival_id']))][["festival_id","축제명","축제설명"]]


# #### 크롤링 과정
# - 축제명을 네이버 뉴스에 검색
# - 상위 5개 뉴스 헤드라인과 미리보기 문단을 크롤링
# - 데이터 프레임을 새로 만들어 축제명을 키로 하여 관련 글귀를 저장

# #### 2019년 데이터의 경우 축제명 끝에 2019가 달려있었기 때문에 이를 제거해주는 작업을 해줌

# In[20]:


target_festival["축제명_수정"]=target_festival["축제명"].map(lambda x : x[:-4])


# ### B.축제 키워드 크롤링 - 불러오기

# #### 2015,2016년 크롤링

# In[44]:


target_festag = pd.DataFrame()
for j in range(len(target_festival["축제명_수정"])) :
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + str(target_festival["축제명_수정"].iloc[j])
    res = requests.get(url=url)

    soup = BeautifulSoup(res.text,"html.parser")
    test = []
    
    for i in range(10) :
        temp = soup.select("#sp_nws"+str(i)+" > dl > dd:nth-of-type(2)")
        
        #temp = soup.select("a._sp_each_url")
        test.append(str(temp))
    target_festag = target_festag.append(pd.DataFrame(np.array([target_festival["축제명_수정"].iloc[j],test]).reshape(1,-1)))
    time.sleep(1)


# ## 2.자연어 처리

# ### A.뉴스 키워드 자연어 처리

# In[45]:


kkma = Kkma()


# In[47]:


target_festag.columns = ["축제명_수정","축제주요내용"]


# In[48]:


target_festag.index= range(len(target_festag))


# In[49]:


target_festag_nouns = target_festag


# In[50]:


for i in range(len( target_festag)) :
    container =  target_festag["축제주요내용"][i]
    target_festag_nouns["축제주요내용"][i] = kkma.nouns(''.join(container))


# In[122]:


#pd.DataFrame(['축제'] + list(keyword['축제'].values)).rename(columns={0:'keyword'}).to_csv("keyword.csv", encoding='cp949', index=False)
keyword = pd.read_csv("keyword.csv", encoding='cp949')


# In[126]:


target_tag = dict()
for i in keyword['keyword'] :
    #print(i)
    tmp_tag_list = []
    for j in target_festag_nouns["축제주요내용"]:
        tmp_tag_list.append(i in j)
    target_tag[i] = tmp_tag_list


# In[127]:


target_tag = pd.DataFrame(target_tag).applymap(int)


# In[128]:





# ## 클러스터 예측

# In[129]:


model = joblib.load("festival_age_prediction.pkl")


# In[135]:


target_festival['클러스터'] = model.predict(target_tag).astype(int)


# ## DB에 추가

# In[137]:


def insert_values_to_table(db_path, table_nm, column_info, data):
    con = sqlite3.connect(db_path, timeout=100)
      
    for i in range(data.shape[0]):
        cur = con.cursor()
        cur.execute("INSERT INTO {} Values {};".format(table_nm, str(tuple(data.iloc[i].values)).replace('nan', 'NULL')))
        cur.close()
    
    con.commit()
    con.close()


# In[139]:


db_path = "SEOUL_FESTIVAL.db"
table_nm = "FESTIVAL_CLUSTER"
column_info = "festival_id INTEGER, 축제명 TEXT, 클러스터 INTEGER"
data = target_festival[['festival_id', '축제명', '클러스터']]

insert_values_to_table(db_path, table_nm, column_info, data)


# In[142]:


con = sqlite3.connect(db_path, timeout=100)
cur = con.cursor()
cur.execute('SELECT * FROM {}'.format(table_nm))
ff = cur.fetchall()
cur.close()

