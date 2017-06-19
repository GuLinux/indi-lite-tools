#!/usr/bin/python

import os
import sys
import math

def binned_exposure_calc(l_exp, binning):
    return l_exp * 3.0 / math.pow(binning, 2)

def total_exposure_count(total_exp_time, l_rgb_ratio, l_single_exposure, rgb_single_exposure):
    l_exposure_total = total_exp_time/2 * l_rgb_ratio
    rgb_exposure_total = total_exp_time/2/l_rgb_ratio 
    return {
        'L_exposure': l_exposure_total,
        'RGB_exposure': rgb_exposure_total,
        'L_exposure_count': l_exposure_total/l_single_exposure,
        'RGB_exposure_count': rgb_exposure_total / 3 / rgb_single_exposure 
    }
       
