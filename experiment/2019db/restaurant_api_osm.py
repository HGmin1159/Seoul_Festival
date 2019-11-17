import requests
import json


overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
node["amenity"="restaurant"](37.413294,126.734086,37.715133,127.269311);
out;
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()


with open('restaurant_osm.json', 'w') as f:
    json.dump(data, f)
