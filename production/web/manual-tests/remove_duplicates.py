import json

d_list = [129, 201, 246, 247, 248]

with open("2019.json", encoding="utf-8") as f:
    lst_of_dicts = json.load(f)

filtered = []

for festival in lst_of_dicts:
    if festival["id"] in d_list:
        i = festival["id"]
        print(f"Removing { i }")
    else:
        filtered.append(festival)

with open("2019n.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(filtered, ensure_ascii=False))
