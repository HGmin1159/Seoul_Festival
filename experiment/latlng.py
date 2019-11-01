import pandas as pd

pathfrom = "데이터전처리/2015_축제_위경도 추가.csv"
pathto = "experiment/2015_축제_위경도 추가_수정.csv"


df = pd.read_csv(pathfrom, encoding="utf-8")

t = df['x'] < df['y']
x = df['x'] * ~t + df['y'] * t
y = df['x'] * t + df['y'] * ~t
df['x'] = x
df['y'] = y

df.to_csv(pathto, encoding="utf-8")

