import json
res = []
temp = []
seen = False
pathfrom = "experiment/festag19.csv"
pathto = "experiment/festag19.json"
with open(pathfrom, encoding="utf-8") as f:
    headers = list(map(lambda x: x.rstrip(), f.readline().split(',')))[1:]
    for line in f:
        if '"' in line:
            seen = not seen
        if not seen:
            if temp:
                temp.append(line.strip())
                line = ' '.join(temp)
                line = list(map(lambda x: x.strip().strip('"'), line.split(',')))[1:]
                res.append(dict(zip(headers, line)))
                temp = []
            else:
                line = list(map(lambda x: x.strip().strip('"'), line.split(',')))[1:]
                res.append(dict(zip(headers, line)))
        else:
            temp.append(line.strip())

with open(pathto, 'w', encoding="utf-8") as f:
    f.write(json.dumps(res, ensure_ascii=False))
       
# for i in res:
#     if '"' in i["축제명"]:
#         print(i, '\n')

# for i in res:
#     print(i, '\n')