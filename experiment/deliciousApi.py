import sqlite3
import pandas as pd
import numpy as np
import requests

conn = sqlite3.connect("experiment/2015_festival.db")
c = conn.cursor()

apikey = "<appkey here>"
url = "https://dapi.kakao.com/v2/local/search/category.json"

pathfrom = "experiment/2015_축제_위경도 추가_수정.csv"
# pathto = "experiment/2015_축제_위경도 추가_수정.csv"

df = pd.read_csv(pathfrom, encoding="utf-8")

def getApi(lng, lat, page):
    """
    in: fl, fl, int
    out: dict"""
    rsp = requests.get(url,
                       params={"category_group_code": "FD6", 'x': str(
                           lng), 'y': str(lat), "radius": 500, "page": page},
                       headers={"Authorization": "KakaoAK " + apikey}
                       )
    if rsp.status_code != 200:
        raise Exception(rsp.status_code)
    return rsp.json()

def db_session_add(doc, pk):
    for d in doc:
        t = []
        for k, v in d.items():
            if k != "distance" and k != "id":
                t.append(v)
            else:
                t.append(int(v))
        t.append(pk)
        c.execute('INSERT INTO restaurants VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', tuple(t))

for i in df.index:
    if df.iloc[i, 3] > 0: # 좌표가 있으면
        page = 1
        rsp = getApi(df.iloc[i,3], df.iloc[i,4], page)
        while not rsp["meta"]["is_end"]:
            doc = rsp["documents"]
            db_session_add(doc, i)
            page += 1
            rsp = getApi(df.iloc[i,3], df.iloc[i,4], page)
        doc = rsp["documents"]
        db_session_add(doc, i)

conn.commit()
        