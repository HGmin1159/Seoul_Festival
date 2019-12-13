from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r'/restaurants/*': {"origins": r"^https:\/\/seoul-festival.*\.now\.sh"}})

KEYS = ('festival_id', 'restaurants_id', 'distance',
        "id", "place_name", "category_name",
        "category_group_code", "category_group_name",
        "phone", "address_name",
        "road_address_name",
        "x", "y", "place_url"
        )

def fetch_res(fes_id):
    conn = sqlite3.connect("SEOUL_FESTIVAL.db")
    c = conn.cursor()
    c.execute("""SELECT *
                FROM (SELECT *
                        FROM festival_restaurant
                        WHERE festival_id = ?) AS fr
                JOIN restaurant_info AS r
                ON fr.restaurants_id = r.id
                ORDER BY distance;
                """, (fes_id, ))
    lst = [dict(zip(KEYS, row)) for row in c]
    conn.close()
    return lst

@app.route('/restaurants/<id>')
def res(id):
    return jsonify(fetch_res(id))