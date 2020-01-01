#!/usr/bin/python3

# %% [markdown]
# # 연령 클러스터 예측

# %%
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import sqlite3

import time
from konlpy.corpus import kolaw
from konlpy.tag import Kkma
import nltk
import konlpy

import pickle
import joblib

def db_add_festival(nparr, table_nm, con):
    cur = con.cursor()
    a = tuple(None if pd.isnull(j) else str(j) for j in tuple(nparr))
    cur.execute(f"INSERT INTO {table_nm} Values ({','.join(['?']*len(a))});", a)
    cur.close()

db_path = "SEOUL_FESTIVAL.db"
table_nm = "FESTIVAL_INFO"
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute('PRAGMA table_info({})'.format(table_nm))
table_columns = [i[1] for i in cur]

cur.execute('SELECT * FROM FESTIVAL_CLUSTER')
cluster_before = pd.DataFrame(cur.fetchall(), columns=['festival_id', '축제명', '클러스터'])
cur.close()
# print(cluster_before['festival_id'].values[-1])
with open("last_id.txt", 'w') as f:
    f.write(str(cluster_before['festival_id'].values[-1]))


# %%
cur = con.cursor()
cur.execute('SELECT * FROM FESTIVAL_info')
festival_updated = pd.DataFrame(cur.fetchall(), columns=table_columns)
cur.close()
con.close()


# %%
# DB에서 가져오기
target_festival = festival_updated.loc[festival_updated['festival_id'].isin(set(festival_updated['festival_id']) - set(cluster_before['festival_id']))][["festival_id","축제명","축제설명"]]

# %% [markdown]
# #### 크롤링 과정
# - 축제명을 네이버 뉴스에 검색
# - 상위 5개 뉴스 헤드라인과 미리보기 문단을 크롤링
# - 데이터 프레임을 새로 만들어 축제명을 키로 하여 관련 글귀를 저장
# %% [markdown]
# #### 2019년 데이터의 경우 축제명 끝에 2019가 달려있었기 때문에 이를 제거해주는 작업을 해줌

# %%
target_festival["축제명_수정"]=target_festival["축제명"].map(lambda x : x[:-4])

# %% [markdown]
# ### B.축제 키워드 크롤링 - 불러오기
# %% [markdown]
# #### 2015,2016년 크롤링

# %%
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

# %% [markdown]
# ## 2.자연어 처리
# %% [markdown]
# ### A.뉴스 키워드 자연어 처리

# %%
kkma = Kkma()


# %%
target_festag.columns = ["축제명_수정","축제주요내용"]


# %%
target_festag.index= range(len(target_festag))


# %%
target_festag_nouns = target_festag


# %%
for i in range(len( target_festag)) :
    container =  target_festag["축제주요내용"][i]
    target_festag_nouns["축제주요내용"][i] = kkma.nouns(''.join(container))


# %%
#pd.DataFrame(['축제'] + list(keyword['축제'].values)).rename(columns={0:'keyword'}).to_csv("keyword.csv", encoding='cp949', index=False)
keyword = pd.read_csv("keyword.csv", encoding='cp949')


# %%
target_tag = dict()
for i in keyword['keyword'] :
    #print(i)
    tmp_tag_list = []
    for j in target_festag_nouns["축제주요내용"]:
        tmp_tag_list.append(i in j)
    target_tag[i] = tmp_tag_list


# %%
target_tag = pd.DataFrame(target_tag).applymap(int)


# %%
target_tag_old = pd.read_csv("target_tag.csv", index_col=0)
target_tag_old.to_csv("target_tag_old.csv")


# %%
target_tag_new = target_tag_old.append(target_tag, ignore_index=True)


# %%
target_tag_new.to_csv("target_tag.csv")

# %% [markdown]
# ## 클러스터 예측

# %%
model = joblib.load("festival_age_prediction.pkl")


# %%
target_festival['클러스터'] = model.predict(target_tag).astype(int)

# %% [markdown]
# ## DB에 추가

# %%
def insert_values_to_table(db_path, table_nm, column_info, data):
    con = sqlite3.connect(db_path, timeout=100)
      
    for i in range(data.shape[0]):
        db_add_festival(data.iloc[i].values, table_nm, con)
    
    con.commit()
    con.close()


# %%
db_path = "SEOUL_FESTIVAL.db"
table_nm = "FESTIVAL_CLUSTER"
column_info = "festival_id INTEGER, 축제명 TEXT, 클러스터 INTEGER"
data = target_festival[['festival_id', '축제명', '클러스터']]

insert_values_to_table(db_path, table_nm, column_info, data)


# %%
con = sqlite3.connect(db_path, timeout=100)
cur = con.cursor()
cur.execute('SELECT * FROM {}'.format(table_nm))
ff = cur.fetchall()
cur.close()
con.close()
