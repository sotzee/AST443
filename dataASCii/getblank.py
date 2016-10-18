# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 22:07:55 2016

@author: Tianqi
"""

from astropy.io import ascii
import numpy as np

data_1=ascii.read('processed_flat.00000100.FIT_clean.new+.cat')
data_1.remove_rows(range(np.size(data_1)))
data_1.add_row([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])
ascii.write(data_1, 'blank.cat')