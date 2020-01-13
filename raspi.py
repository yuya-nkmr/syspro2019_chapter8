# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time
import RPi.GPIO as GPIO
import smbus
import datetime
import json
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/syspro-chapter8.json"

cred = credentials.Certificate('/home/pi/syspro-chapter8.json')
firebase_admin.initialize_app(cred)
i2c = smbus.SMBus(1)
address = 0x48

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.HIGH)
time.sleep(1)
GPIO.output(14, GPIO.LOW)

db = firestore.Client()

# コールバック関数を作成する
def on_snapshot(doc_snapshot, changes, read_time):
    for change in changes:
        print(u'New cmd: {}'.format(change.document.id))
        led = change.document.to_dict()["led"]
        print(u'LED: {}'.format(led))
        if led == "ON":
            print "ON"
            # ONにする処理
        elif led == "OFF":
            print "OFF"
            # OFFにする処理


on_ref = db.collection('led').where(u'led', u'==', u'ON')
off_ref = db.collection('led').where(u'led', u'==', u'OFF')

# 監視を開始する
doc_watch = on_ref.on_snapshot(on_snapshot)
doc_watch = off_ref.on_snapshot(on_snapshot)

# 温度センサの管理を行う部分
# 温度センサと接続できたら，「'''」を取る
'''
while True:
    block = i2c.read_i2c_block_data(address, 0x00, 12)
    temp = (block[0] << 8 | block[1]) >> 3
    if(temp >= 4096):
        temp -= 8192
    print("Temperature:%6.2f" % (temp / 16.0))
    data = {"temp": temp / 16.0}
    db.collection('temperature').document(str(datetime.datetime.now())).set(data)
    time.sleep(1)
'''

# 温度センサと接続できないうちはこの無限ループを使う
while True:
    pass
