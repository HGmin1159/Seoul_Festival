#!/usr/bin/python3
import sqlite3, requests, json
from collections import OrderedDict

# last_id = int(input())
with open("last_id.txt") as f:
    last_id = int(f.readline())

KEYS = ['id', 'place_name', 'category_name', 'category_group_code',
        'category_group_name', 'phone', 'address_name', 'road_address_name',
        'x', 'y', 'place_url', 'distance']

url = "https://dapi.kakao.com/v2/local/search/category.json"

with open("config.json") as f:
    apikey = json.load(f)["APIKEY"]

db_path = "SEOUL_FESTIVAL.db"

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
    c.execute("""SELECT festival_id, x, y 
                FROM FESTIVAL_INFO
                WHERE x > 0 AND festival_id > ?;""", (last_id, ))
    lst = [dict(zip(('id', 'x', 'y'), row)) for row in c]
    return lst

con = sqlite3.connect(db_path)

cur = con.cursor()

# create_restaurants(cur)

# create_festival_restaurants(cur)

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
