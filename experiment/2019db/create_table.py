import sqlite3
import pandas as pd


pathfrom = "festival_crawling_2019.xlsx"
pathto = "2019.db"
df = pd.read_excel("festival_crawling_2019.xlsx", index_col=0)
df.drop(columns="img", inplace=True)
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
                "id" INTEGER PRIMARY KEY,
                "title" TEXT,
                "개최지역" TEXT,
                "개최기간" TEXT,
                "축제성격" TEXT,
                "관련 누리집" TEXT,
                "축제장소" TEXT,
                "요금" TEXT,
                "소요시간" TEXT,
                "연령제한" TEXT,
                "주최/주관기관" TEXT,
                "문의" TEXT,
                "explanation" TEXT,
                "오시는 길" TEXT,
                "부대행사" TEXT,
                "축제장소_수정" TEXT,
                "축제명_수정" TEXT,
                "address_name" TEXT,
                "x" REAL,
                "y" REAL,
                "road_address_name" TEXT,
                "place_url" TEXT
                )
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
    # print(df)
    create_festival()
    alter_festival()
    create_restaurants()
    create_festival_restaurants()
    conn.close()
