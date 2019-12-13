import sqlite3, json, re

pathfrom = "SEOUL_FESTIVAL.db"
pathto = "2019.json"

FKEYS = ('id', 'name', 'x', 'y', 'period', 'explanation', 'cluster', 'region', 'place')

def fetch_fes():
    conn = sqlite3.connect(pathfrom)
    c = conn.cursor()
    c.execute("""SELECT festival_info.festival_id, festival_info.축제명, x, y, 개최기간, 축제설명, 클러스터, 개최지역, 축제장소
                FROM FESTIVAL_INFO, FESTIVAL_CLUSTER
                WHERE festival_info.festival_id = festival_cluster.festival_id AND x > 0;""")
    lst = [dict(zip(FKEYS, row)) for row in c]
    conn.close()
    return lst

def attach_man_ratio(lst):
    with open('output.csv') as f:
        f.readline()
        for line in f:
            a = line.split(',')
            for fes in lst:
                if fes['id'] == int(a[0].strip('"')):
                    fes['man'] = float(a[-1])

lst = fetch_fes()

attach_man_ratio(lst)

arr = []
for f in lst:
    matches = re.finditer(r'\b(\d{1,2})(\.|월)\s?(\d{1,2})', f['period'])
    early = (13, 0)
    for m in matches:
        temp = (int(m.group(1)), int(m.group(3)))
        if temp < early:
            early = temp
    if early < (13, 0):
        f['date'] = {'month': early[0], 'day': early[1]}
        arr.append(f)
arr.sort(key=lambda f: f['date']['month']*40 + f['date']['day'])


with open(pathto, 'w', encoding="utf-8") as f:
    f.write(json.dumps(arr, ensure_ascii=False))

# for i in range(10):
#     print(lst[i])

# with open('output.csv') as f:
#     f.readline()
#     for line in f:
#         print(line)
