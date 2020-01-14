# https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings

from difflib import SequenceMatcher
import json


WLIST = [33]

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def get_max_date(dates: list) -> (int, int):
    """
    dates: [
        {"year": int, "month": int, "day": int},
        ...,
    ]
    Example:
    dates: [{'year': 2019, 'month': 12, 'day': 21}, {'year': 2019, 'month': 12, 'day': 29}]"""
    res = sorted(dates, key=lambda d: d["year"] * 13 + d["month"])
    if len(res) == 0:
        return (-1, -1)
    return (res[-1]["year"], res[-1]["month"])

with open("2019.json", encoding="utf-8") as f:
    lst_of_dicts = json.load(f)

# fail = False

for i in lst_of_dicts:
    for j in lst_of_dicts:
        if i["id"] > j["id"] and\
        get_max_date(i["date"]) == get_max_date(j["date"]) and\
        similar(i["explanation"], j["explanation"]) > 0.7 and\
        j["id"] not in WLIST:
            # fail = True
            print(similar(i["explanation"], j["explanation"]))
            print(i)
            print(j)
            print()
