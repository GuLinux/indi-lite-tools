import sys
sys.path.append('../../') # Change this to the module installation path

import functools
from pyindi_sequence import SequenceBuilder

sb = SequenceBuilder('M42', upload_path = '/tmp/M42')

def set_binning(bin_mode):
    sb.camera.set_number('CCD_BINNING', {'HOR_BIN': bin_mode, 'VER_BIN': bin_mode})

sb.set_camera('CCD Simulator')
sb.set_filter_wheel('Filter Simulator')
sb.add_filter_wheel_step('Luminosity')

sb.add_message_step('Setting bin to 1x1')
sb.add_function(functools.partial(set_binning, 1))

sb.add_sequence('Light', exposure=3, count=2)
sb.add_filter_wheel_step('Red')

sb.add_user_confirmation_prompt('Please cover your camera lens for Dark Frames (1x1). Press Enter to continue')
sb.add_auto_dark()


sb.add_user_confirmation_prompt('Remove camera cover and press Enter')
sb.add_message_step('Setting bin to 3x3')
sb.add_function(functools.partial(set_binning, 3))


sb.add_sequence('Red', exposure=7, count=2)
sb.add_filter_wheel_step('Green')
sb.add_sequence('Green', exposure=5, count=2)
sb.add_filter_wheel_step('Blue')
sb.add_sequence('Blue', exposure=6, count=2)
sb.add_user_confirmation_prompt('Please cover your camera lens for Dark Frames (3x3). Press Enter to continue')
sb.add_auto_dark()
sb.add_shell_command('gzip -1 /tmp/M42/*.fits', shell=True)

# The following line shows what happens when you run a shell command returning error
# sb.add_shell_command('gzipaa', shell=True, abort_on_failure = True)
# sb.add_user_confirmation_prompt('we should never see this, since the previous command should return an error')

print(sb)
sb.start()
