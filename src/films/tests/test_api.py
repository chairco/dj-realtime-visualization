# films/tests/test_api.py
import requests
import json


url_mixin = 'http://localhost:8000/films/filmsmixin/'
url_films = 'http://localhost:8000/films/films/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
payload = {
    'pic': 'Image_20180731',
    'pic_url': '/20180731/00002.png',
    'content_type': 1,
    'rs232_time': '2018-07-27T13:13:00+08:00',
    'film_gaps': {
        'gap0': 1.72,
        'gap1': 1.96,
        'gap2': 1.97,
        'gap3': 2.12,
        'gap4': 2.02,
        'gap5': 1.72
    },
}


data = json.dumps(payload)
r = requests.post(url_films, json=payload)
print(r.status_code)
print(r.json())
