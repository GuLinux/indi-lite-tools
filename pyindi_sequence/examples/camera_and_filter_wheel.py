import sys
sys.path.append('../../') # Change this to the module installation path

from pyindi_sequence import SequenceBuilder

sb = SequenceBuilder('M42', upload_path = '/tmp/M42')
sb.set_camera('CCD Simulator')
sb.set_filter_wheel('Filter Simulator')
sb.add_filter_wheel_step('Luminosity')
sb.add_sequence('Light', exposure=3, count=2)
sb.add_filter_wheel_step('Red')
sb.add_sequence('Red', exposure=7, count=2)
sb.add_filter_wheel_step('Green')
sb.add_sequence('Green', exposure=5, count=2)
sb.add_filter_wheel_step('Blue')
sb.add_sequence('Blue', exposure=6, count=2)
sb.add_user_confirmation_prompt('Please cover your camera lens for Dark Frames. Press Enter to continue')
sb.add_auto_dark()
sb.add_shell_command('gzip -1 /tmp/M42/*.fits', shell=True)

# The following line shows what happens when you run a shell command returning error
# sb.add_shell_command('gzipaa', shell=True, abort_on_failure = True)
# sb.add_user_confirmation_prompt('we should never see this, since the previous command should return an error')

print(sb)
sb.start()
