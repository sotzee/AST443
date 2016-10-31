# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:39:33 2016

@author: Tianqi,Nam
"""


from astropy.io import ascii
import sys
import matplotlib.pyplot as plt
import numpy as np

def normalizeFlux(data,aper_num,omit_range):
    # Input data catalog, aperture number and omitting range
    numer = 0.
    denom = 0.
    count = 0
    flux = 'FLUX_APER_'+str(aper_num)
    fluxerr = 'FLUXERR_APER_'+str(aper_num)
    # Calculating weighted mean
    for i in range(len(data['NUMBER'])):
        if i in omit_range:
            continue
        else:
            numer += data[i][flux]/(data[i][fluxerr]**2)
            denom += 1./(data[i][fluxerr]**2)
            count += 1
    flux_ave = numer/denom
    data[flux] = data[flux]/flux_ave
    data[fluxerr] = data[fluxerr]/flux_ave
    return data

# Normalize target flux, omiting the 'eclipsing' interval
data_target=normalizeFlux(ascii.read('target.cat'),2,range(50,269))

data_guiding=list()
fig = plt.figure(figsize=(15,10))
for i in range(10):
    # Normalize reference stars fluxes
    data_guiding.append(normalizeFlux(ascii.read('guiding'+str(i+1)+'.cat'),2,[]))
    # Filtering bad images by setting error to 1.e40
    dummy = data_guiding[i]['FLUX_APER_2']
    for j in range(len(dummy)):
        if (dummy[j] > 1.03) or (dummy[j] < 0.97):
            data_guiding[i]['FLUXERR_APER_2'][j] = 1.e40
    # Plot reference stars fluxes
    ax = fig.add_subplot(3,4,i+1)
    ax.errorbar(data_guiding[i]['NUMBER'],data_guiding[i]['FLUX_APER_2'],yerr=data_guiding[i]['FLUXERR_APER_2'],fmt='o')
    ax.set_ylim([0.95,1.05])
#plt.savefig('refstar.eps',format='eps',dpi=1000)
plt.close()

data_guiding_flux_master_list=list()
data_guiding_error_master_list=list()

# Calculating weighted mean of different reference stars
for i in [0,1,3,4,5]:
    data_guiding_flux_master_list.append(data_guiding[i]['FLUX_APER_2']/data_guiding[i]['FLUXERR_APER_2']**2)
    data_guiding_error_master_list.append(1/data_guiding[i]['FLUXERR_APER_2']**2)

data_guiding_flux_master=data_guiding_flux_master_list[0]
data_guiding_error_master=data_guiding_error_master_list[0]
for i in [1,2,3,4]:
    data_guiding_flux_master=data_guiding_flux_master+data_guiding_flux_master_list[i]
    data_guiding_error_master=data_guiding_error_master+data_guiding_error_master_list[i]
data_guiding_flux_master=data_guiding_flux_master/data_guiding_error_master

# Calculating flux ratio
transit_ratio=data_target['FLUX_APER_2']/data_guiding_flux_master

########### Let's find average of the two plateau############
# 1st one: <45 mins and >155 mins
# 2nd one: 75 mins < t < 125 mins
r1 = 0.
r2 = 0.
numpt1 = 0
numpt2 = 0
for i in range(len(transit_ratio)):
    time = data_target['NUMBER'][i]/60000.
    if (time < 45.) or (time > 155.):
        r1 += transit_ratio[i]
        numpt1 += 1
    elif (time > 75.) and (time < 125.):
        r2 += transit_ratio[i]
        numpt2 += 1
r1 = r1/numpt1
r2 = r2/numpt2
print 'numpts: ',numpt1,numpt2

# Rerun loop to find errors
rerr1 = 0.
rerr2 = 0.
numpt1 = 0
numpt2 = 0
for i in range(len(transit_ratio)):
    time = data_target['NUMBER'][i]/60000.
    if (time < 45.) or (time > 155.):
        rerr1 += (transit_ratio[i]-r1)**2
        numpt1 += 1
    elif (time > 75.) and (time < 125.):
        rerr2 += (transit_ratio[i]-r2)**2
        numpt2 += 1
rerr1 = np.sqrt(rerr1/numpt1/(numpt1-1.))
rerr2 = np.sqrt(rerr2/numpt2/(numpt2-1.))

print 'numpts: ',numpt1,numpt2
print 'r1, rerr1: ',r1,rerr1
print 'r2, rerr2: ',r2,rerr2
print 'Flux ratio: ',r2/r1                                

# Normalize ratio
transit_ratio = transit_ratio/r1

############### Bin it up - 5 minutes bins ##################
binWidth = 5. #mins
num_bin = int(np.ceil(max(data_target['NUMBER'])/60000./binWidth))
bindata = np.zeros([num_bin,2])
binerror = np.zeros(num_bin)
# Index for transit_ratio
j = 0
for i in range(num_bin):
    num_point = 0
    while int(data_target['NUMBER'][j]/60000./binWidth) < (i+1):
        bindata[i,1] += transit_ratio[j]
        bindata[i,0] += data_target['NUMBER'][j]/60000.
        num_point += 1
        j+=1
        # The last image
        if j == len(transit_ratio):
            break
    bindata[i,1] = bindata[i,1]/num_point
    bindata[i,0] = bindata[i,0]/num_point

# Rerun loop to get errors
j = 0
for i in range(num_bin):
    num_point = 0
    while int(data_target['NUMBER'][j]/60000./binWidth) < (i+1):
        binerror[i] += (transit_ratio[j]-bindata[i,1])**2
        num_point += 1
        j+=1
        if j == len(transit_ratio):
            break
    binerror[i] = np.sqrt(binerror[i]/num_point/(num_point-1.))
##################################################################

# Plot all data points and binned data points with error bars
plt.plot(data_target['NUMBER']/60000.,transit_ratio,'o',label='wasp-2')
plt.errorbar(bindata[:,0],bindata[:,1],yerr=binerror,fmt='o',label='wasp-2')
plt.legend()
plt.xlabel('Time(min)')
plt.ylabel('Normalized flux ratio')
#plt.savefig('final_lightcurve.eps',format='eps',dpi=1000)
plt.show()
