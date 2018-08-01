# films/tests/test_api.py
import requests
import json
import random
import alog
from datetime import datetime

r = requests.post('http://localhost:8000/films/filmseq/')
resp = r.json()
seqid = resp.get('id')
alog.info(f"{r.status_code}, {r.json()}")


url = 'http://localhost:8000/films/films/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {
    'pic': None,
    'pic_url': None,
    'content_type': 1,
    'seq': seqid,
    'cam': None,
    'rs232_time': None,
    'len_ret': None,
    'gap_ret': None,
    'film_gaps': {},
    'film_lens': {}
}


cam0 = payload.copy()
# cam0 data
cam0['pic'] = f"Image_{datetime.now().strftime('%Y%m%d')}"
cam0['pic_url'] = f"/{datetime.now().strftime('%Y%m%d')}/0000{random.randint(1,2)}.png"
cam0['cam'] = 0
cam0['rs232_time'] = '2018-07-27T13:13:00+08:00'
cam0['len_ret'] = '0'
cam0['gap_ret'] = '0'
cam0['film_gaps'] = {'gap0': 1.72, 'gap1': 1.96,'gap2': 1.97,
                    'gap3': 2.12, 'gap4': 2.02, 'gap5': 1.72}
cam0['film_lens'] = {'pink': 45.06, 'orange': 44.32, 'yellow': 45.23,
                    'green': 45.12, 'blue': 45.56}

# insert_data_0
r = requests.post(url, json=json.dumps(cam0))
alog.info(f"{r.status_code}, {r.json()}")


cam0 = payload.copy()
# cam1 data
cam0['pic'] = f"Image_{datetime.now().strftime('%Y%m%d')}"
cam0['pic_url'] = f"/{datetime.now().strftime('%Y%m%d')}/0000{random.randint(1,2)}.png"
cam0['cam'] = 1
cam0['rs232_time'] = '2018-07-27T13:13:00+08:00'
cam0['len_ret'] = '0'
cam0['gap_ret'] = '0'
cam0['film_gaps'] = {'gap0': 2.12, 'gap1': 1.94,'gap2': 2.07,
                    'gap3': 2.10, 'gap4': 2.01, 'gap5': 1.83}
cam0['film_lens'] = {'pink': 45.36, 'orange': 44.12, 'yellow': 44.23,
                    'green': 45.12, 'blue': 45.76}

# insert_data_1
r = requests.post(url, json=json.dumps(cam0))
alog.info(f"{r.status_code}, {r.json()}")




