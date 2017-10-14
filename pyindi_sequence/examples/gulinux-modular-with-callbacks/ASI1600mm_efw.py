import sys
import os
from pyindi_sequence import SequenceBuilder, ShellCommandStep
import requests
import functools
import json
import time, datetime
import textwrap
import __main__

#import urllib3

#urllib3.disable_warnings()

ASI_BIAS_EXPOSURE=0.000032
FILTER_LUMINANCE=1
FILTER_RED=2
FILTER_GREEN=3
FILTER_BLUE=4
FILTER_DARK=5

buzzer_config = { 'enabled': False, 'default_duration': 10 }

# get session name from script name. This way, when you copy this script to, let's say, 2017-05-10-M42.py, your session name will be 'M42'

SESSION_NAME=os.path.splitext(__main__.__file__)[0].replace(' ', '_')

print('Session name: {}'.format(SESSION_NAME))

sb = SequenceBuilder(SESSION_NAME, camera_name='ZWO CCD ASI1600MM')
sb.set_filter_wheel('ASI EFW')


def set_oled_message(title, text, wrap=True):
    if wrap:
        text = textwrap.fill(text, 21)
    requests.put('http://localhost:5100/oled', json={'text': text, 'title': title})

def clear_oled():
    requests.delete('http://localhost:5100/oled')

def send_event(event_type, event_text, notify=False, require_interaction=False):
    requests.put('http://localhost:5100/events', json={'type': event_type, 'text': event_text, 'notify': notify, 'require_interaction': require_interaction})

def enable_buzzer(enable, default_duration=10):
    buzzer_config['enabled'] = enable
    buzzer_config['default_duration'] = default_duration

def send_buzzer(pattern, loop=True, duration=None):
    if buzzer_config['enabled']:
        requests.put('http://localhost:5100/buzzer', json={'pattern': pattern, 'loop': loop, 'duration': duration})

def clear_buzzer():
    requests.delete('http://localhost:5100/buzzer')

def add_prompt_step(message):
    sb.add_function(functools.partial(set_oled_message, 'Confirm', message))
    sb.add_function(functools.partial(send_event, 'User confirmation', message, notify=True, require_interaction=True))
    sb.add_function(functools.partial(send_buzzer, [{"frequency": 1500, "duration": 0.5}, {"frequency": 0, "duration": 0.2}], duration=buzzer_config['default_duration']))
    sb.add_user_confirmation_prompt(message)
    sb.add_function(clear_buzzer)
    sb.add_function(clear_oled)

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
        set_oled_message('Error', str(sys.exc_info()[1]))
        send_event('Error', str(sys.exc_info()[1]), notify=True, require_interaction=True)
        send_buzzer([{"frequency": 2500, "duration": 0.2}, {"frequency": 0, "duration": 0.2}])
        print("Unexpected error:", sys.exc_info()[0])
        raise

def __on_sequence_starting(sequence):
  send_event('Sequence starting', str(sequence))

def __on_sequence_ended(sequence):
  send_event('Sequence finished', str(sequence), notify=True)

def __send_sequence_item_led(sequence, item):
  code = 'u'
  filter_codes = { 'light': 'L' ,'luminance': 'L', 'red': 'r', 'green': 'G', 'blue': 'b', 'dark': 'd', 'bias': 'o', 'offset': 'o'}
  for pattern in filter_codes:
    if pattern in sequence.name.lower():
      code = filter_codes[pattern]
  remaining_seconds = str(sequence.remaining_seconds())
  remaining_seconds = remaining_seconds[0:5] if '.' in remaining_seconds else remaining_seconds[0:4]
  set_oled_message(sequence.name, 'shot {}/{}/{}\nTime {}/{}/{}'.format(
        sequence.finished,
        sequence.remaining_shots(),
        sequence.count,
        sequence.shot_seconds(),
        sequence.remaining_seconds(),
        sequence.total_seconds()
      ), wrap=False)

def __on_sequence_item_starting(sequence, item):
  send_event('Shoot', 'Shoot started {}/{}, exposure: {}s, remaining: {}, {}s'
             .format(item+1, sequence.count, sequence.exposure, sequence.remaining_shots(), sequence.remaining_seconds()))
  __send_sequence_item_led(sequence, item)

def __on_sequence_item_ended(sequence, item, file_name):
    send_event('Shoot', 'Shoot finished {}/{}, filename: {}, exposure: {}s, remaining: {}, {}s'
             .format(item+1, sequence.count, file_name, sequence.exposure, sequence.remaining_shots(), sequence.remaining_seconds()))
    __send_sequence_item_led(sequence, item)

def add_sequence(*args, **kwargs):
    seq = sb.add_sequence(*args, **kwargs)
    seq.callbacks.add('on_started', __on_sequence_starting)
    seq.callbacks.add('on_each_started', __on_sequence_item_starting)
    seq.callbacks.add('on_each_finished', __on_sequence_item_ended)
    seq.callbacks.add('on_finished', __on_sequence_ended)


def create_sequence(settings):
    sb.add_message_step('Changing filter wheel to {}'.format(settings['code']))
    sb.add_filter_wheel_step(filter_number=settings['filter'])
    change_settings(settings)
    if 'refocus' in settings and settings['refocus']:
        add_prompt_step('Focus check for {}'.format(settings['name']))
        sb.add_filter_wheel_step(filter_number=FILTER_LUMINANCE)
        change_settings(settings)
    add_sequence(settings['name'], exposure=settings['exp'], count=settings['count'])



def dark_bias(settings, name=None, frame_type='FRAME_DARK'):
    if not name:
        name = settings['name']
    frame_name = 'Dark'
    exposure = settings['exp']
    count = settings['dark']
    if frame_type == 'FRAME_BIAS':
        exposure = ASI_BIAS_EXPOSURE
        frame_name = 'Bias'
        count = settings['bias']

    sb.add_message_step('Taking {} {} frames for sequence {}'.format(count, frame_name.lower(), name))
    sb.add_filter_wheel_step(filter_number=FILTER_DARK)
    change_settings(settings, frame_type=frame_type)
    add_sequence('{0}-{1}-{2}x{2}'.format(frame_name, name, settings['bin']), exposure, count=count, auto_dark = False)


def change_settings(settings, frame_type='FRAME_LIGHT'):
    height = 3520

#    # uncomment the following if you're using an older INDI version, and you get an error using binning = 3
#    if settings['bin'] == 3:
#        height = 3519
    sb.change_camera_settings(binning=settings['bin'], frame_type = frame_type )
    sb.change_camera_settings(
        roi = {'X': 0, 'Y': 0, 'WIDTH': 4656, 'HEIGHT': height},
        compression_format = 'CCD_RAW',
        controls = {
            'HighSpeedMode': 1,
            'HardwareBin': settings['hwbin'],
            'Gain': settings['gain'],
        },
        switches = {'CCD_VIDEO_FORMAT': {'on': ['ASI_IMG_RAW16']}, 'CCD_CONTROLS_MODE': {'on': ['AUTO_BandWidth'], 'off': ['AUTO_Gain']} }
    )


def merge(a, b):
    a = a.copy()
    a.update(b)
    return a
