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


while True:
    try:
        temp = requests.get('http://localhost:5100/temp_humidity')
        if temp.status_code == 200:
            temp_obj = temp.json()
            t = temp_obj['temperature']
            h = temp_obj['humidity']
            text = u'{0:.1f}c.{1:.1f}h'.format(t, h)
            r = requests.put('http://localhost:5100/led', json={'text': text, 'brightness': 0, 'id': 'temp_humidity', 'overwrite': False})
            print('data: {}, response: {}'.format(temp.json(), r))
    except:
        traceback.print_exc()
    time.sleep(interval)
