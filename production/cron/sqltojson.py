#!/usr/bin/python3
import sqlite3, json, re

with open("last_id.txt") as f:
    last_id = int(f.readline())

pathfrom = "SEOUL_FESTIVAL.db"
pathto = "../web/2019.json"

FKEYS = ('id', 'name', 'x', 'y', 'period', 'explanation', 'cluster', 'region', 'place', 'link')

def fetch_fes():
    conn = sqlite3.connect(pathfrom)
    c = conn.cursor()
    c.execute("""SELECT festival_info.festival_id, festival_info.축제명, x, y, 개최기간, 축제설명, 클러스터, 개최지역, 축제장소, 관련_누리집
                FROM FESTIVAL_INFO, FESTIVAL_CLUSTER
                WHERE festival_info.festival_id > ?
                AND x > 0
                AND festival_info.festival_id = festival_cluster.festival_id;""", (last_id, ))
    lst = [dict(zip(FKEYS, row)) for row in c]
    conn.close()
    return lst

def attach_man_ratio(lst):
    with open('output.csv', encoding="utf-8") as f:
        f.readline()
        for line in f:
            a = line.split(',')
            for fes in lst:
                if fes['id'] == int(a[0].strip('"')):
                    fes['man'] = float(a[-1])

lst = fetch_fes()

attach_man_ratio(lst)

for f in lst:
    prev = None
    f['date'] = []
    matches = re.finditer(r'\b((\d{4})(\.|년)\s?)?(\d{1,2})(\.|월)\s?(\d{1,2})', f['period'])
    for m in matches:
        year = int(m.group(2)) if m.group(2) != None else None
        month = int(m.group(4))
        day = int(m.group(6))
        if year != None:
            prev = year
        elif prev != None:
            year = prev
        else:
            year = 2020
        f['date'].append({
            "year": year,
            "month": month,
            "day": day
        })

with open(pathto) as f:
    j = json.load(f)

lst = j + lst

with open(pathto, 'w', encoding="utf-8") as f:
    f.write(json.dumps(lst, ensure_ascii=False))
