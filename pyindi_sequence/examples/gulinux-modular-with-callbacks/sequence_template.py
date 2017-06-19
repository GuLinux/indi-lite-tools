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

def dark_bias(name, count, exposure, binning=1):
    frame_name = 'Dark'
    frame_type = 'FRAME_DARK'
    if exposure == 0:
        exposure = ASI_BIAS_EXPOSURE
        frame_name = 'Bias'
        frame_type = 'FRAME_BIAS'

    sb.add_message_step('Taking {} {} frames for sequence {}'.format(count, frame_name.lower(), name))
    sb.add_filter_wheel_step(filter_number=FILTER_DARK)
    sb.change_camera_settings(binning=binning, frame_type = frame_type)
    add_sequence('{0}-{1}-{2}x{2}'.format(frame_name, name, binning), exposure, count=count, auto_dark = False)

add_prompt_step('Changing camera settings to RAW 16bit, bin 1x1, press Enter to confirm')
change_settings(binning=1)
sb.add_message_step('Changing filter wheel to Luminance')
sb.add_filter_wheel_step(filter_number=FILTER_LUMINANCE)
add_sequence('Light', exposure=LIGHT['exp'], count=LIGHT['count'])

dark_bias('Light', LIGHT_DARK_COUNT, LIGHT['exp'], binning=1)

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
dark_bias('RGB', RGB_DARK_COUNT, RED['exp'], binning=RGB_BINNING)

# Separate dark settings for different r/g/b exposures

#dark_bias('R', RGB_DARK_COUNT, RED['exp'], binning=RGB_BINNING)
#dark_bias('G', RGB_DARK_COUNT, GREEN['exp'], binning=RGB_BINNING)
#dark_bias('B', RGB_DARK_COUNT, BLUE['exp'], binning=RGB_BINNING)


# Bias frames
dark_bias('Light', LIGHT_BIAS_COUNT, 0, binning=1)
dark_bias('RGB', RGB_BIAS_COUNT, 0, binning=RGB_BINNING)

print(sb)
start_sequence()

