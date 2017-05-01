import sys
sys.path.append('../../') # Change this to the module installation path

from pyindi_sequence import SequenceBuilder

sb = SequenceBuilder('M42', upload_path = '/tmp/')
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
sb.add_auto_datk()

sb.start()
