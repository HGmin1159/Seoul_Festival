import sqlite3
import pandas as pd
import requests
from collections import OrderedDict

conn = sqlite3.connect("experiment/2015_festival.db")
c = conn.cursor()

apikey = "<appkey>"
url = "https://dapi.kakao.com/v2/local/search/category.json"

pathfrom = "experiment/2015_축제_위경도 추가_수정.csv"
# pathto = "experiment/2015_축제_위경도 추가_수정.csv"

df = pd.read_csv(pathfrom, encoding="utf-8")
KEYS = ['id', 'place_name', 'category_name', 'category_group_code',
        'category_group_name', 'phone', 'address_name', 'road_address_name',
        'x', 'y', 'place_url', 'distance']


def getApi(lng, lat, page):
    """
    in: fl, fl, int
    out: dict"""
    rsp = requests.get(url,
                       params={"category_group_code": "FD6", 'x': str(
                           lng), 'y': str(lat), "radius": 1000, "page": page},
                       headers={"Authorization": "KakaoAK " + apikey}
                       )
    if rsp.status_code != 200:
        raise Exception(rsp.status_code)
    return rsp.json()


def db_session_add(doc, pk):
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
        c.execute('INSERT INTO festival_restaurants VALUES (?,?,?)',
                  (pk, res_id, dist))
        c.execute(
            'INSERT OR IGNORE INTO restaurants VALUES (?,?,?,?,?,?,?,?,?,?,?)', tuple(t))


for i in df.index:
    if df.iloc[i, 3] > 0:  # 좌표가 있으면
        page = 1
        rsp = getApi(df.iloc[i, 3], df.iloc[i, 4], page)
        while not rsp["meta"]["is_end"]:
            doc = rsp["documents"]
            
            db_session_add(doc, i)
            page += 1
            rsp = getApi(df.iloc[i, 3], df.iloc[i, 4], page)
        doc = rsp["documents"]
        
        db_session_add(doc, i)

conn.commit()
