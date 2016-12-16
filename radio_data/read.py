# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:57:19 2016

@author: sotzee
"""

import matplotlib.pyplot as plt
import numpy as np

plt.subplot(3,2,1)
f = open('suninter1.cmbl', 'r')

data=list()
for line in f:
    data.append(float(line))

x=np.linspace(0,100,np.size(data))
plt.plot(x,data)

plt.subplot(3,2,2)
f = open('suninter2.cmbl', 'r')

data=list()
for line in f:
    data.append(float(line))

x=np.linspace(0,100,np.size(data))
plt.plot(x,data)

plt.subplot(3,2,3)
f = open('suninter3.cmbl', 'r')

data=list()
for line in f:
    data.append(float(line))

x=np.linspace(0,100,np.size(data))
plt.plot(x,data)

plt.subplot(3,2,4)
f = open('suninter4.cmbl', 'r')

data=list()
for line in f:
    data.append(float(line))

x=np.linspace(0,100,np.size(data))
plt.plot(x,data)

plt.subplot(3,2,5)
f = open('suninter5.cmbl', 'r')

data=list()
for line in f:
    data.append(float(line))

x=np.linspace(0,100,np.size(data))
plt.plot(x,data)

plt.subplot(3,2,6)
f = open('suninter6.cmbl', 'r')

data=list()
for line in f:
    data.append(float(line))

x=np.linspace(0,100,np.size(data))
plt.plot(x,data)

#==============================================================================
# plt.subplot(1,2,2)
# f = open('natlogansam_radiolab2/sun21.cmbl', 'r')
# 
# data=list()
# for line in f:
#     data.append(float(line))
# 
# x=np.linspace(0,100,np.size(data))
# plt.plot(x,data)
#==============================================================================

data=np.array(data)
zero=data.max()
peak=data.min()
maximum=zero-peak

index_max=data.argmin()

n=index_max
while data[n]<data[n+1]:
    n+=1
minimum=zero-data[n]
V1=(maximum-minimum)/(maximum+minimum)

n=index_max
while data[n]<data[n-1]:
    n-=1
minimum=zero-data[n]
V2=(maximum-minimum)/(maximum+minimum)
print [V1,V2]