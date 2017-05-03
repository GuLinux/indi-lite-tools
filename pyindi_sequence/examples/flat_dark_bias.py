import sys
sys.path.append('../../') # Change this to the module installation path

from pyindi_sequence import SequenceBuilder

sb = SequenceBuilder('M42', camera_name='CCD Simulator', upload_path = '/tmp/M42')
def set_flat_exposure(secs_str):
    flat_exposure = float(secs_str)
    sb.add_sequence('Flat', exposure=flat_exposure, count=3)
    

sb.add_user_confirmation_prompt('Press Enter to start Shooting')
sb.add_sequence('RGB', exposure=4, count=2)
sb.add_user_confirmation_prompt('Please cover your camera lens for Dark and Bias frames. Press Enter to continue')
sb.add_auto_dark(count=2)
sb.add_sequence('Bias', exposure=sb.camera.exposure_range()['minimum'], count=2)
sb.add_message_step('Please point your camera to a flat field generator (wall, daylight sky, flat field panel)')
sb.add_user_confirmation_prompt('When ready, enter the exposure for the flat frames and press Enter to start shooting\nFlat exposure (secs): ', on_input = set_flat_exposure)


print(sb)
sb.start()
