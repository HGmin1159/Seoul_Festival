import urllib.request
from contextlib import closing
import pandas as pd
import re


def getfile(url, filename, timeout=45):
    with closing(urllib.request.urlopen(url, timeout=timeout)) as fp:
        block_size = 1024 * 8
        block = fp.read(block_size)
        if block:
            with open(filename, 'wb') as out_file:
                out_file.write(block)
                while True:
                    block = fp.read(block_size)
                    if not block:
                        break
                    out_file.write(block)
        else:
            raise Exception('nonexisting file or connection error')


df = pd.read_excel("festival_crawling_2019.xlsx", index_col=0)

pat = re.compile(r'src="(/attachFiles/.+\.(jpg|JPG))"')

for i in df.index:
    match = pat.search(df.iat[i, 1])
    path = match.group(1)
    path = "https://www.mcst.go.kr" + path
    getfile(url=path, filename=str(i)+".jpg")
