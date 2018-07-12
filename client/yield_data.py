#-*- coding: utf-8 -*-
import websocket
import random
import json
import schedule
import time
import alog

from datetime import datetime

ip = "localhost:8000"
addr = f"ws://{ip}/ws/films/async/hello/" 


def ws_connect(addr):
    ws = websocket.WebSocket()
    ws.connect(addr)
    return ws


def yield_information():
    # create instance
    ws = ws_connect(addr)
    # create information
    yields = random.randint(4000, 10000)
    pass_data = random.randint(4000, yields)
    yield_rate = f"{pass_data / yields:.2%}"
    message = f"產量:{yields}, yield rate={yield_rate}"
    now_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    alog.info(f"Now: {now_time}")
    info = json.dumps({'message':message, 'user':'guest', 'now_time':now_time})

    alog.info(f"Send: {info}")
    # send websocket
    ws.send(info)
    ws.close()


schedule.every(0.1).minutes.do(yield_information)


while True:
    schedule.run_pending()
    time.sleep(1)