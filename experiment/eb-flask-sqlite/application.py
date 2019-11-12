from flask import Flask, render_template, jsonify, redirect
import sqlite3

application = Flask(__name__)

KEYS = ('festival_id', 'restaurants_id', 'distance',
        "id", "place_name", "category_name",
        "category_group_code", "category_group_name",
        "phone", "address_name",
        "road_address_name",
        "x", "y", "place_url"
        )


def fetch_fes():
    conn = sqlite3.connect("2015_festival.db")
    c = conn.cursor()
    c.execute("SELECT id, 축제명, x, y FROM festival;")
    lst = [row for row in c]
    conn.close()
    return lst


def fetch_res(fes_id):
    conn = sqlite3.connect("2015_festival.db")
    c = conn.cursor()
    c.execute("""
                SELECT *
                FROM (SELECT *
                        FROM festival_restaurants
                        WHERE festival_id = ?) AS fr
                JOIN restaurants AS r
                ON fr.restaurants_id = r.id
                ORDER BY distance;
                """, (fes_id, ))
    lst = [dict(zip(KEYS, row)) for row in c]
    conn.close()
    return lst


@application.route('/')
def web():
    return redirect("static/index.html")


@application.route('/festival')
def fes():
    lst = fetch_fes()
    return jsonify(lst)


@application.route('/restaurants/<id>')
def res(id):
    lst = fetch_res(id)
    return jsonify(lst)


if __name__ == '__main__':
    application.run()
