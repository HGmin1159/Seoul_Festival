#!/usr/bin/python3
import urllib.request
from contextlib import closing
import sqlite3
import re

with open("last_id.txt") as f:
    last_id = int(f.readline())

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

def fetch_fes(c):
    """
    in: cursor
    out: list
    """
    c.execute("""SELECT festival_id, img
                FROM FESTIVAL_INFO
                WHERE festival_id > ?;""", (last_id, ))
    lst = [dict(zip(('id', 'img'), row)) for row in c]
    return lst

con = sqlite3.connect("SEOUL_FESTIVAL.db")
c = con.cursor()
lst = fetch_fes(c)
con.close()

pat = re.compile(r'src="(/attachFiles/.+\.(jpg|JPG))"')

for i in lst:
    match = pat.search(i['img'])
    path = match.group(1)
    path = "https://www.mcst.go.kr" + path
    getfile(url=path, filename="../web/public/img/"+str(i['id'])+".jpg")
