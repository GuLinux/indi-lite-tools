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
RGB_BINNING = 2
RGB_DARK_COUNT = LIGHT_DARK_COUNT
RGB_BIAS_COUNT = LIGHT_BIAS_COUNT


def change_settings(binning=1, frame_type='FRAME_LIGHT'):
    height = 3520

    # deal with INDI asi roi bug, solved in june 2017 - remove after rasbpberry daily builds get the updated solution
    if binning == 3:
        height = 3519
    sb.change_camera_settings(binning = binning, frame_type = frame_type )
    sb.change_camera_settings(
        roi = {'X': 0, 'Y': 0, 'WIDTH': 4656, 'HEIGHT': height},
        compression_format = 'CCD_RAW',
        controls = {
            'HighSpeedMode': 1,
            'HardwareBin': 1,
            'Gain': 140,
        },
        switches = {'CCD_VIDEO_FORMAT': {'on': ['ASI_IMG_RAW16']}, 'CCD_CONTROLS_MODE': {'on': ['AUTO_BandWidth'], 'off': ['AUTO_Gain']} }
    )

def dark_bias(name, dark_count, bias_count, dark_exposure = None, binning=1, auto_dark=False, skip_bias=False):
    sb.add_message_step('Taking dark/bias frames - changing filter wheel to the Dark filter position')
    sb.add_filter_wheel_step(filter_number=FILTER_DARK)
    if not skip_bias:
        change_settings(binning=binning, frame_type='FRAME_BIAS')
        add_sequence('Bias-{0}-{1}x{1}'.format(name, binning), ASI_BIAS_EXPOSURE, count=bias_count, auto_dark = False)
    if auto_dark or not dark_exposure:
        sb.add_auto_dark(count = LIGHT_DARK_COUNT, name='Dark-{0}-{1}x{1}'.format(name, binning))
    else:
        sb.change_camera_settings(frame_type = 'FRAME_DARK')
        add_sequence('Dark-{0}-{1}x{1}'.format(name, binning), dark_exposure, count=dark_count, auto_dark = False)


add_prompt_step('Changing camera settings to RAW 16bit, bin 1x1, press Enter to confirm')
change_settings(binning=1)
sb.add_message_step('Changing filter wheel to Luminance')
sb.add_filter_wheel_step(filter_number=FILTER_LUMINANCE)
add_sequence('Light', exposure=LIGHT['exp'], count=LIGHT['count'])

# Bias/Dark in between light and RGB - comment this to take darks/bias all at the end
dark_bias('Light', LIGHT_DARK_COUNT, LIGHT_BIAS_COUNT, binning=1, auto_dark=True)

change_settings(binning=RGB_BINNING)
sb.add_message_step('Changing filter wheel to the Red filter position')
sb.add_filter_wheel_step(filter_number=FILTER_RED)
add_sequence('Red', exposure=RED['exp'], count=RED['count'])

sb.add_message_step('Changing wheel to the Green filter position')
sb.add_filter_wheel_step(filter_number=FILTER_GREEN)
add_sequence('Green', exposure=GREEN['exp'], count=GREEN['count'])

sb.add_message_step('Changing filter wheel to the Blue filter position')
sb.add_filter_wheel_step(filter_number=FILTER_BLUE)
add_sequence('Blue', exposure=BLUE['exp'], count=BLUE['count'])


# Bias/Dark with auto mode - comment this, and uncomment the lines below, to take all darks, including Luminance, after all sequences are done 
dark_bias('RGB', RGB_DARK_COUNT, RGB_BIAS_COUNT, binning=RGB_BINNING, auto_dark=True)


#dark_bias('Light', LIGHT_DARK_COUNT, LIGHT_BIAS_COUNT, binning=1, dark_exposure=LIGHT['exp'])
#dark_bias('RGB', RGB_DARK_COUNT, RGB_BIAS_COUNT, binning=RGB_BINNING, dark_exposure=RED['exp'])
##The followings are for different dark exposures between R, G, B
##dark_bias('R', RGB_DARK_COUNT, RGB_BIAS_COUNT, binning=RGB_BINNING, dark_exposure=RED['exp'])
##dark_bias('G', RGB_DARK_COUNT, RGB_BIAS_COUNT, binning=RGB_BINNING, dark_exposure=GREEN['exp'], skip_bias=True)
##dark_bias('B', RGB_DARK_COUNT, RGB_BIAS_COUNT, binning=RGB_BINNING, dark_exposure=BLUE['exp'], skip_bias=True)

print(sb)
start_sequence()

