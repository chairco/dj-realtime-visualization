# films/tests/test_api.py
import requests
import json
import random
from datetime import datetime

r = requests.post('http://localhost:8000/films/filmseq/')
resp = r.json()
seqid = resp.get('id')
print(seqid)

url = 'http://localhost:8000/films/films/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# basic
payload_1 = {
    'pic': f"Image_{datetime.now().strftime('%Y%m%d')}",
    'pic_url': f"/{datetime.now().strftime('%Y%m%d')}/0000{random.randint(1,2)}.png",
    'content_type': 1,
    'seq': seqid,
    'cam': 0,
    'rs232_time': '2018-07-27T13:13:00+08:00',
    'len_ret': '1',
    'gap_ret': '0',
    'film_gaps': {
        'gap0': 1.72,
        'gap1': 1.96,
        'gap2': 1.97,
        'gap3': 2.12,
        'gap4': 2.02,
        'gap5': 1.72
    },
    'film_lens': {
        'pink': 45.06,
        'orange': 44.32,
        'yellow': 45.23,
        'green': 45.12,
        'blue': 45.56
    }
}


payload_2 = {
    'pic': f"Image_{datetime.now().strftime('%Y%m%d')}",
    'pic_url': f"/{datetime.now().strftime('%Y%m%d')}/0000{random.randint(1,2)}.png",
    'content_type': 1,
    'seq': seqid,
    'cam': 1,
    'rs232_time': '2018-07-27T13:13:00+08:00',
    'len_ret': '1',
    'gap_ret': '0',
    'film_gaps': {
        'gap0': 2.12,
        'gap1': 1.96,
        'gap2': 1.97,
        'gap3': 2.12,
        'gap4': 2.02,
        'gap5': 1.72
    },
    'film_lens': {
        'pink': 45.06,
        'orange': 44.32,
        'yellow': 45.23,
        'green': 45.12,
        'blue': 45.56
    }
}


# insert_data_1
data = json.dumps(payload_1)
r = requests.post(url, json=data)
print(r.status_code)
print(r.json())


# insert_data_2
data = json.dumps(payload_2)
r = requests.post(url, json=data)
print(r.status_code)
print(r.json())




