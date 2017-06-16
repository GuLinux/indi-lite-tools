import sys
import os
import inspect
from pyindi_sequence import SequenceBuilder, ShellCommandStep
import requests
import functools
import json
#import urllib3

#urllib3.disable_warnings()

ASI_BIAS_EXPOSURE=0.00032
FILTER_LUMINANCE=1
FILTER_RED=2
FILTER_GREEN=3
FILTER_BLUE=4
FILTER_DARK=5

# get session name from script name. This way, when you copy this script to, let's say, 2017-05-10-M42.py, your session name will be 'M42'

_frame = inspect.stack()[1]
_module = inspect.getmodule(_frame[0])
SESSION_NAME=os.path.splitext(os.path.basename(_module.__file__))[0].replace(' ', '_')

print('Session name: {}'.format(SESSION_NAME))

requests.put('http://localhost:5100/led_brightness', json={'brightness': 0})

sb = SequenceBuilder(SESSION_NAME, camera_name='ZWO CCD ASI1600MM')
sb.set_filter_wheel('EFW')


def set_led_text(text):
    requests.put('http://localhost:5100/led/text/sequence', json={'text': text, 'duration': 2})

def send_event(event_type, event_text):
  requests.put('http://localhost:5100/events', json={'type': event_type, 'text': event_text})

def add_prompt_step(message, led_text = 'USER'):
    sb.add_function(functools.partial(set_led_text, led_text))
    sb.add_function(functools.partial(send_event, 'User confirmation', message))
    sb.add_user_confirmation_prompt(message)
    sb.add_function(functools.partial(set_led_text, ''))

def __save_coordinates():
    c = requests.get('http://localhost:5100/coordinates')
    if c.status_code == 200:
      with open(os.path.join(sb.upload_path, 'coordinates.json'), 'w') as j:
        json.dump(c.json(), j)

def start_sequence():
    #sb.add_shell_command('gzip -1 {0}/*.fits'.format(sb.upload_path), shell=True)
    sb.add_shell_command('sync', shell=True)

    add_prompt_step('Finished. Press Enter to quit')
    try:
        __save_coordinates()
        sb.start()
        __save_coordinates()
    except:
        set_led_text('ERROR')
        send_event('Error', str(sys.exc_info()[1]))
        print("Unexpected error:", sys.exc_info()[0])
        raise

def __on_sequence_starting(sequence):
  send_event('Sequence starting', str(sequence))

def __on_sequence_ended(sequence):
  send_event('Sequence finished', str(sequence))

def __on_sequence_item_starting(sequence, item):
  send_event('Shoot', 'Shoot started {}/{}, exposure: {}s, remaining: {}, {}s'
             .format(item+1, sequence.count, sequence.exposure, sequence.remaining_shots(), sequence.remaining_seconds()))

  code = 'u'
  filter_codes = { 'light': 'L' ,'luminance': 'L', 'red': 'r', 'green': 'G', 'blue': 'b', 'dark': 'd', 'bias': 'o', 'offset': 'o'}
  for pattern in filter_codes:
    if pattern in sequence.name.lower():
      code = filter_codes[pattern]
  remaining_seconds = str(sequence.remaining_seconds())
  remaining_seconds = remaining_seconds[0:5] if '.' in remaining_seconds else remaining_seconds[0:4]
  set_led_text('{}.{}.{}'.format(code, str(sequence.remaining_shots()).zfill(3), remaining_seconds.zfill(4)))

def __on_sequence_item_ended(sequence, item):
  send_event('Shoot', 'Shoot finished {}/{}, exposure: {}s, remaining: {}, {}s'
             .format(item+1, sequence.count, sequence.exposure, sequence.remaining_shots(), sequence.remaining_seconds()))

def add_sequence(*args, **kwargs):
    seq = sb.add_sequence(*args, **kwargs)
    seq.callbacks.add('on_started', __on_sequence_starting)
    seq.callbacks.add('on_each_started', __on_sequence_item_starting)
    seq.callbacks.add('on_each_finished', __on_sequence_item_ended)
    seq.callbacks.add('on_finished', __on_sequence_ended)
