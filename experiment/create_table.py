import sqlite3
import pandas as pd

pathfrom = "experiment/2015_축제_위경도 추가_수정.csv"
pathto = "experiment/2015_festival.db"

df = pd.read_csv(pathfrom, encoding="utf-8")

conn = sqlite3.connect(pathto)


def create_festival():
    df.to_sql("festival", conn, if_exists="replace")


def alter_festival():
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=off;")
    c.execute("BEGIN TRANSACTION;")
    c.execute("ALTER TABLE festival RENAME TO _festival_old;")
    c.execute('''
                CREATE TABLE "festival" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "축제명" TEXT,
                "address_name" TEXT,
                "place_name" TEXT,
                "x" REAL,
                "y" REAL,
                "road_address_name" TEXT,
                "place_url" TEXT,
                "연번" INTEGER,
                "시도명" TEXT,
                "시군구명" TEXT,
                "시작일" TEXT,
                "종료일" TEXT,
                "축제주요내용" TEXT,
                "주최/주관
                (담당자 연락처)" TEXT,
                "최초개최년도
                및 횟수" TEXT,
                "축제예산(안)
                (합  계)" TEXT,
                "국비" REAL,
                "도비" REAL,
                "시군비" REAL,
                "기타" REAL,
                "축제종류" TEXT
                ); 
    ''')
    c.execute('''INSERT INTO festival
                SELECT *
                FROM _festival_old;''')
    c.execute("DROP TABLE _festival_old;")
    c.execute("COMMIT;")
    c.execute("PRAGMA foreign_keys=on;")
    conn.commit()


def create_restaurants():
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS restaurants")
    c.execute('''CREATE TABLE "restaurants" (
            "id" INTEGER PRIMARY KEY,
            "place_name" TEXT,
            "category_name" TEXT,
            "category_group_code" TEXT,
            "category_group_name" TEXT,
            "phone" TEXT,
            "address_name" TEXT,
            "road_address_name" TEXT,
            "x" REAL,
            "y" REAL,
            "place_url" TEXT
    );''')
    conn.commit()


def create_festival_restaurants():
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS festival_restaurants")
    c.execute('''CREATE TABLE festival_restaurants (
        festival_id INTEGER,
        restaurants_id INTEGER,
        distance INTEGER,
        FOREIGN KEY(festival_id) REFERENCES festival(id) ON DELETE SET NULL,
        FOREIGN KEY(restaurants_id) REFERENCES restaurants(id) ON DELETE SET NULL
    )''')
    conn.commit()


if __name__ == "__main__":
    create_festival()
    alter_festival()
    create_restaurants()
    create_festival_restaurants()
