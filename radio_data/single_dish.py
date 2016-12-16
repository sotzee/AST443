# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:38:20 2016

@author: sotzee
"""

import matplotlib.pyplot as plt
import numpy as np

f_sat = open('natlogansam_radiolab/sat1.cmbl', 'r')
f_sun = open('natlogansam_radiolab2/sun1.cmbl', 'r')

data_sat=list()
for line in f_sat:
    data_sat.append(float(line))

data_sun=list()
for line in f_sun:
    data_sun.append(float(line))

print np.size(data_sat)
print np.size(data_sun)
x_sat=np.linspace(0,100,np.size(data_sat))
x_sun=np.linspace(0,100,np.size(data_sun))
plt.subplot(2,2,1)
plt.plot(x_sat,data_sat)
plt.subplot(2,2,2)
plt.plot(x_sun,data_sun)

x_sat=np.take(x_sat,range(int(np.size(data_sat)*0.4)+1,int(np.size(data_sat)*0.7)+1))
sat_bg=np.take(data_sat,range(int(np.size(data_sat)*0.7)+1,int(np.size(data_sat)*1.0)))
data_sat=np.take(data_sat,range(int(np.size(data_sat)*0.4)+1,int(np.size(data_sat)*0.7)+1))-sat_bg.mean()
plt.subplot(2,2,3)
plt.plot(x_sat,data_sat)

x_sun1=np.take(x_sun,range(int(np.size(data_sun)*0.2)+1,int(np.size(data_sun)*0.4)))
sun_bg1=np.take(data_sun,range(int(np.size(data_sun)*0.2)+1,int(np.size(data_sun)*0.4)))
x_sun2=np.take(x_sun,range(int(np.size(data_sun)*0.7)+1,int(np.size(data_sun)*1.0)))
sun_bg2=np.take(data_sun,range(int(np.size(data_sun)*0.7)+1,int(np.size(data_sun)*1.0)))
x_sun_bg=np.concatenate((x_sun1,x_sun2),axis=0)
data_sun_bg=np.concatenate((sun_bg1,sun_bg2),axis=0)
polyfit=np.polyfit(x_sun_bg,data_sun_bg,4)
plt.subplot(2,2,2)
#plt.plot(x_sun_bg,data_sun_bg)
plt.plot(x_sun_bg,polyfit[0]*x_sun_bg**4+polyfit[1]*x_sun_bg**3+polyfit[2]*x_sun_bg**2+polyfit[3]*x_sun_bg+polyfit[4])

plt.subplot(2,2,4)
x_sun=np.take(x_sun,range(int(np.size(data_sun)*0.4)+1,int(np.size(data_sun)*0.7)+1))
data_sun=np.take(data_sun,range(int(np.size(data_sun)*0.4)+1,int(np.size(data_sun)*0.7)+1))-(polyfit[0]*x_sun**4+polyfit[1]*x_sun**3+polyfit[2]*x_sun**2+polyfit[3]*x_sun+polyfit[4])
plt.plot((x_sun-55.0)*np.cos(23.0/180*np.pi)/100*40,data_sun/data_sun.min())
plt.plot((x_sat-.2-55.0)*np.cos(40.0/180*np.pi)/100*40,data_sat/data_sat.min())

