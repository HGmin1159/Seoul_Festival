import sqlite3
import pandas as pd

pathfrom = "experiment/2015_festival.db"
folder = "experiment/2015_festival_db/"

conn = sqlite3.connect(pathfrom)

tables = ["festival", "restaurants", "festival_restaurants"]

for table in tables:
    df = pd.read_sql(f"SELECT * from {table}", conn)
    df.to_csv(f"{folder}{table}.csv", encoding="cp949", index=False)
