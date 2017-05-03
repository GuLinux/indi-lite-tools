import sys
sys.path.append('../../') # Change this to the module installation path

from pyindi_sequence import SequenceBuilder



sb = SequenceBuilder('M42', camera_name='CCD Simulator', upload_path = '/tmp/M42')

def camera_settings():
    sb.camera.set_switch('CCD_COMPRESSION', ['CCD_RAW'])

sb.add_message_step('Adjusting camera settings')
sb.add_function(camera_settings)
sb.add_user_confirmation_prompt('Press Enter to start Shooting')
sb.add_sequence('RGB', exposure=3, count=2)
sb.add_user_confirmation_prompt('Please cover your camera lens for Dark Frames. Press Enter to continue')
sb.add_auto_dark()

print(sb)
sb.start()
