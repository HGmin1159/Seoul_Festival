import sqlite3
import pandas as pd

pathfrom = "experiment/2015_축제_위경도 추가_수정.csv"
pathto = "experiment/2015_festival.db"

df = pd.read_csv(pathfrom, encoding="utf-8")

conn = sqlite3.connect(pathto)

def create_festival():
    df.to_sql("festival", conn, if_exists="replace")

def create_restaurants():
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS restaurants")
    c.execute('''CREATE TABLE "restaurants" (
        "address_name" TEXT,
            "category_group_code" TEXT,
            "category_group_name" TEXT,
            "category_name" TEXT,
            "distance" INTEGER,
            "id" INTEGER PRIMARY KEY,
            "phone" TEXT,
            "place_name" TEXT,
            "place_url" TEXT,
            "road_address_name" TEXT,
            "x" REAL,
            "y" REAL
    );''')
    conn.commit()

def create_festival_restaurants():
    c = conn.cursor()
    c.execute('''CREATE TABLE festival_restaurants (
        festival_id INTEGER,
        restaurants_id INTEGER,
        FOREIGN KEY(festival_id) REFERENCES festival(id) ON DELETE SET NULL,
        FOREIGN KEY(restaurants_id) REFERENCES restaurants(id) ON DELETE SET NULL
    )''')
    conn.commit()

if __name__ == "__main__":
    create_festival()
    create_restaurants()
    create_festival_restaurants()