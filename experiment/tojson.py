import json
res = []
temp = []
seen = False
with open("A-team/experiment/festag16.txt", encoding="utf-8") as f:
    headers = list(map(lambda x: x.rstrip(), f.readline().split(',')))[1:]
    for line in f:
        if '"' in line:
            seen = not seen
        if not seen:
            if temp:
                temp.append(line.rstrip())
                line = ''.join(temp)
                line = list(map(lambda x: x.rstrip(), line.split(',')))[1:]
                res.append(dict(zip(headers, line)))
                temp = []
            else:
                line = list(map(lambda x: x.rstrip(), line.split(',')))[1:]
                res.append(dict(zip(headers, line)))
        else:
            temp.append(line.rstrip())

with open("A-team/experiment/festag16.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(res, ensure_ascii=False))
       
# for i in res:
#     print(i, '\n')
