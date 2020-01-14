import json


d_list = [58, 86, 241, 243, 250]

with open("2019.json", encoding="utf-8") as f:
    lst_of_dicts = json.load(f)

for festival in lst_of_dicts:
    if festival["id"] in d_list:
        i = festival["id"]
        url = festival["link"]
        print(f"Removing { i }: { url }")
        festival["link"] = ""

with open("2019n.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(lst_of_dicts, ensure_ascii=False))
