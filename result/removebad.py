# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 22:07:55 2016

@author: Tianqi
"""

from astropy.io import ascii
import numpy as np

removelist=range(87)
removelist=list(np.array(removelist)+321)
for i in range(10):
    data=ascii.read('guiding'+str(i+1)+'.cat')
    data.remove_rows(removelist)
    ascii.write(data, 'guiding'+str(i+1)+'.cat')

data=ascii.read('target.cat')
data.remove_rows(removelist)
ascii.write(data,'target.cat')
