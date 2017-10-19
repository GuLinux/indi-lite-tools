#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import sys
import os
import traceback

interval = 5
if len(sys.argv) > 1:
    interval = int(sys.argv[1])

print('Using {}s polling interval'.format(interval))

def send_string(text):
    return requests.put('http://localhost:5100/led', json={'text': text, 'brightness': 0, 'id': 'temp_humidity', 'overwrite': False})

while True:
    try:
        send_string(time.strftime('T%H.%M.%S', time.localtime()))
        time.sleep(1)
        send_string(time.strftime('T%H.%M.%S', time.localtime()))

        temp = requests.get('http://localhost:5100/temp_humidity')
        if temp.status_code == 200:
            temp_obj = temp.json()
            t = temp_obj['temperature']
            h = temp_obj['humidity']
            text = u'{0:.1f}c.{1:.1f}h'.format(t, h)
            time.sleep(1)
            r = send_string(text)
            print('data: {}, response: {}'.format(temp.json(), r))
            time.sleep(interval)
    except:
        traceback.print_exc()

