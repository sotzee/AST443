# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:39:33 2016

@author: Tianqi
"""

from astropy.io import ascii
#import numpy as np
import matplotlib.pyplot as plt
plt.cla()

data_target=ascii.read('target.cat')
data_guiding=list()
for i in range(10):
    data_guiding.append(ascii.read('guiding'+str(i+1)+'.cat'))

data_guiding_flux_master_list=list()
data_guiding_error_master_list=list()

for i in [0,2,3,4,5,7,8]:
    #plt.plot(data_guiding[i]['NUMBER'],data_guiding[i]['FLUX_APER_2'],label='calibration'+str(i+1))
    data_guiding_flux_master_list.append(data_guiding[i]['FLUX_APER_2']/data_guiding[i]['FLUXERR_APER_2']**2)
    data_guiding_error_master_list.append(1/data_guiding[i]['FLUXERR_APER_2']**2)

data_guiding_flux_master=data_guiding_flux_master_list[0]
data_guiding_error_master=data_guiding_error_master_list[0]
for i in [1,2,3,4,5,6]:
    data_guiding_flux_master=data_guiding_flux_master+data_guiding_flux_master_list[i]
    data_guiding_error_master=data_guiding_error_master+data_guiding_error_master_list[i]
data_guiding_flux_master=data_guiding_flux_master/data_guiding_error_master
#plt.plot(data_target['NUMBER'],data_guiding_flux_master,label='calibration master')
#plt.plot(data_target['NUMBER'],data_target['FLUX_APER_2'],label='wasp-2')

transit_ratio=data_target['FLUX_APER_2']/data_guiding_flux_master
plt.plot(data_target['NUMBER'],transit_ratio,label='wasp-2')

plt.legend()
plt.xlabel('time')
plt.ylabel('ratio')
plt.ylim([1.45,1.55])
plt.show()