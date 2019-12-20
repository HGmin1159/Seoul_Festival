import json

d = {}
with open('clt_labels.csv') as f:
    f.readline()
    for line in f:
        a = line.split(',')
        d.update({int(a[0]): list(map(float, a[1:]))})

with open('../web/clt_labels.json', 'w', encoding="utf-8") as f:
    f.write(json.dumps(d, ensure_ascii=False))