import json, requests


with open("2019.json", encoding="utf-8") as f:
    lst_of_dicts = json.load(f)

for i in lst_of_dicts:
    url = i['link']
    if len(url) == 0:
        continue
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(resp)
            print(i)
            print()
    except requests.exceptions.ConnectionError as err:
        print(err)
        print(i)
        print()