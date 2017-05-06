import sys
import os
sys.path.append(os.path.join(os.environ['HOME'], 'indi-lite-tools')) # Change this to the module installation path

from pyindi_sequence import SequenceBuilder, ShellCommandStep


ASI_BIAS_EXPOSURE=0.00032

# get session name from script name. This way, when you copy this script to, let's say, 2017-05-10-M42.py, your session name will be 'M42'
SESSION_NAME=os.path.splitext(os.path.basename(__file__))[0].replace(' ', '_')

LIGHT = {'exp': 1, 'count': 1}
LIGHT_DARK_COUNT = LIGHT['count']
LIGHT_BIAS_COUNT = LIGHT_DARK_COUNT
RED = {'exp': 1, 'count': 1}
GREEN = RED
BLUE = RED
RGB_DARK_COUNT = LIGHT_DARK_COUNT
RGB_BIAS_COUNT = LIGHT_DARK_COUNT




sb = SequenceBuilder(SESSION_NAME, camera_name='ZWO CCD ASI1600MM')

# ledctl is a shell script setting leds status on a Raspberry Pi
def add_prompt_step(message):
    sb.add_shell_command('ledctl led0 blink', shell=True)
    sb.add_user_confirmation_prompt(message)
    sb.add_shell_command('ledctl led0 blink 100 1900', shell=True)



#sb.camera.set_number('CCD_FRAME', {'WIDTH': 4656, 'HEIGHT': 3520}) # Full ROI
add_prompt_step('Changing camera settings to RAW 16bit, bin 1x1, press Enter to confirm')
sb.change_camera_settings(
    roi = {'X': 0, 'Y': 0, 'WIDTH': 4656, 'HEIGHT': 3519}, # workaround for ASI 1600: when using bin 3x3, you need to reduce ROI
    compression_format = 'CCD_RAW',
    binning = 1,
    frame_type = 'FRAME_LIGHT',
    controls = {'HighSpeedMode': 1, 'HardwareBin': 0},
    switches = {'CCD_VIDEO_FORMAT': {'on': ['ASI_IMG_RAW16']}, 'CCD_CONTROLS_MODE': {'on': ['AUTO_BandWidth'], 'off': ['AUTO_Gain']} }
)

add_prompt_step('Change your filter wheel to the Luminance filter position, and press Enter')
sb.add_sequence('Light', exposure=LIGHT['exp'], count=LIGHT['count'])

add_prompt_step('Please cover your camera lens for Dark Frames. Press Enter to continue')
sb.change_camera_settings(frame_type = 'FRAME_BIAS')
sb.add_sequence('Bias-1x1', ASI_BIAS_EXPOSURE, count=LIGHT_BIAS_COUNT, auto_dark = False)
sb.add_auto_dark(count = LIGHT_DARK_COUNT)


sb.add_message_step('Setting bin to 3x3')
sb.change_camera_settings(frame_type = 'FRAME_LIGHT', binning = 3)

add_prompt_step('Change your filter wheel to the Red filter position, and press Enter')
sb.add_sequence('Red', exposure=RED['exp'], count=RED['count'])

add_prompt_step('Change your filter wheel to the Green filter position, and press Enter')
sb.add_sequence('Green', exposure=GREEN['exp'], count=GREEN['count'])

add_prompt_step('Change your filter wheel to the Blue filter position, and press Enter')
sb.add_sequence('Blue', exposure=BLUE['exp'], count=BLUE['count'])

add_prompt_step('Please cover your camera lens for Dark Frames. Press Enter to continue')
sb.change_camera_settings(frame_type = 'FRAME_BIAS')
sb.add_sequence('Bias-3x3', ASI_BIAS_EXPOSURE, count=RGB_BIAS_COUNT, auto_dark = False)
sb.add_auto_dark(count = RGB_DARK_COUNT)

sb.add_shell_command('gzip -1 {0}/*.fits'.format(sb.upload_path), shell=True)
sb.add_shell_command('ledctl led0 trigger mmc0', shell=True)
sb.add_shell_command('sync', shell=True)


print(sb)
try:
    sb.start()
except:
    ShellCommandStep('ledctl led0 blink', shell=True).run()
    print("Unexpected error:", sys.exc_info()[0])
    raise
