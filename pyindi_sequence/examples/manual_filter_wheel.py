import sys
sys.path.append('../../') # Change this to the module installation path

from pyindi_sequence import SequenceBuilder

sb = SequenceBuilder('M42', camera_name='CCD Simulator', upload_path = '/tmp/M42')
sb.add_user_confirmation_prompt('Change your filter wheel to the Luminance filter position, and press Enter')
sb.add_sequence('Light', exposure=3, count=2)
sb.add_user_confirmation_prompt('Change your filter wheel to the Red filter position, and press Enter')
sb.add_sequence('Red', exposure=7, count=2)
sb.add_user_confirmation_prompt('Change your filter wheel to the Green filter position, and press Enter')
sb.add_sequence('Green', exposure=5, count=2)
sb.add_user_confirmation_prompt('Change your filter wheel to the Blue filter position, and press Enter')
sb.add_sequence('Blue', exposure=6, count=2)
sb.add_user_confirmation_prompt('Please cover your camera lens for Dark Frames. Press Enter to continue')
sb.add_auto_dark()

print(sb)
sb.start()
