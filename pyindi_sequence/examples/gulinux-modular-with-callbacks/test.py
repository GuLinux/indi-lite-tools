from ASI1600mm_efw import *

enable_buzzer(False)

LIGHT = {'name': 'Light', 'code': 'L', 'filter': FILTER_LUMINANCE, 'exp': 1, 'count': 1, 'gain': 140, 'dark': 20, 'bias': 50, 'bin': 1, 'hwbin': 0, 'refocus': True}

# not really reliable way to calculate binned exposure
#def binned_rgb_from_luminance(binning):
#    return LIGHT['exp'] * 3.0 / pow(binning, 2)

RED = {'name': 'Red', 'code': 'R', 'filter': FILTER_RED, 'exp': 1, 'count': 1, 'gain': 140, 'dark': 20, 'bias': 50, 'bin': 2, 'hwbin': 0, 'refocus': True}
GREEN = merge(RED, {'name': 'Green', 'code': 'G', 'filter': FILTER_GREEN})
BLUE = merge(RED, {'name': 'Blue', 'code': 'B', 'filter': FILTER_BLUE})


create_sequence(LIGHT)
dark_bias(LIGHT)
create_sequence(RED)
create_sequence(GREEN)
create_sequence(BLUE)

# Bias/Dark with auto mode - comment this, and uncomment the lines below, to take all darks, including Luminance, after all sequences are done 
dark_bias(RED, name='RGB')

# Separate dark settings for different r/g/b exposures
#dark_bias(RED)
#dark_bias(GREEN)
#dark_bias(BLUE)


# Bias frames
dark_bias(LIGHT, frame_type='FRAME_BIAS')
dark_bias(RED, name='RGB', frame_type='FRAME_BIAS')

print(sb)
start_sequence()

