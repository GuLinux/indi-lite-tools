from ASI1600mm_efw import *

LIGHT = {'exp': 1, 'count': 1}

# not really reliable way to calculate binned exposure
#def binned_rgb_from_luminance(binning):
#    return LIGHT['exp'] * 3.0 / pow(binning, 2)

LIGHT_DARK_COUNT = 20
LIGHT_BIAS_COUNT = 50

RED = {'exp': 1, 'count': 1}
GREEN = RED
BLUE = RED
RGB_DARK_COUNT = LIGHT_DARK_COUNT
RGB_BIAS_COUNT = LIGHT_BIAS_COUNT


add_prompt_step('Changing camera settings to RAW 16bit, bin 1x1, press Enter to confirm')
sb.change_camera_settings(binning = 1, frame_type = 'FRAME_LIGHT' )
sb.change_camera_settings(
    roi = {'X': 0, 'Y': 0, 'WIDTH': 4656, 'HEIGHT': 3520},
    compression_format = 'CCD_RAW',
    controls = {'HighSpeedMode': 1, 'HardwareBin': 1},
    switches = {'CCD_VIDEO_FORMAT': {'on': ['ASI_IMG_RAW16']}, 'CCD_CONTROLS_MODE': {'on': ['AUTO_BandWidth'], 'off': ['AUTO_Gain']} }
)

sb.add_message_step('Changing filter wheel to Luminance')
sb.add_filter_wheel_step(filter_number=FILTER_LUMINANCE)
add_sequence('Light', exposure=LIGHT['exp'], count=LIGHT['count'])

sb.add_message_step('Covering camera lens for dark frames')
sb.add_filter_wheel_step(filter_number=FILTER_DARK)
sb.change_camera_settings(frame_type = 'FRAME_BIAS')
add_sequence('Bias-L-1x1', ASI_BIAS_EXPOSURE, count=LIGHT_BIAS_COUNT, auto_dark = False)
sb.add_auto_dark(count = LIGHT_DARK_COUNT, name='Dark-L-1x1')


# Bin 3x3
# sb.add_message_step('Setting bin to 3x3')
# sb.change_camera_settings(frame_type = 'FRAME_LIGHT', binning = 3, roi={'X': 0, 'Y': 0, 'WIDTH': 4656, 'HEIGHT': 3519})

# Bin 2x2
sb.add_message_step('Setting bin to 2x2')
sb.change_camera_settings(frame_type = 'FRAME_LIGHT', binning = 2, roi={'X': 0, 'Y': 0, 'WIDTH': 4656, 'HEIGHT': 3520})


sb.add_message_step('Changing filter wheel to the Red filter position')
sb.add_filter_wheel_step(filter_number=FILTER_RED)
add_sequence('Red', exposure=RED['exp'], count=RED['count'])

sb.add_message_step('Changing wheel to the Green filter position')
sb.add_filter_wheel_step(filter_number=FILTER_GREEN)
add_sequence('Green', exposure=GREEN['exp'], count=GREEN['count'])

sb.add_message_step('Changing filter wheel to the Blue filter position')
sb.add_filter_wheel_step(filter_number=FILTER_BLUE)
add_sequence('Blue', exposure=BLUE['exp'], count=BLUE['count'])

sb.add_message_step('Covering camera for Dark Frames')
sb.add_filter_wheel_step(filter_number=FILTER_DARK)
sb.change_camera_settings(frame_type = 'FRAME_BIAS')
add_sequence('Bias-RGB-3x3', ASI_BIAS_EXPOSURE, count=RGB_BIAS_COUNT, auto_dark = False)
sb.add_auto_dark(name='Dark-RGB-3x3', count = RGB_DARK_COUNT)

print(sb)
start_sequence()
