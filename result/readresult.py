# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:39:33 2016

@author: Tianqi,Nam
"""


from astropy.io import ascii
#import numpy as np
import sys
import matplotlib.pyplot as plt
import numpy as np
#plt.cla()

def normalizeFlux(data,aper_num,omit_range):
    # Input data catalog and keyword
    numer = 0.
    denom = 0.
    count = 0
    flux = 'FLUX_APER_'+str(aper_num)
    fluxerr = 'FLUXERR_APER_'+str(aper_num)
    #print data['NUMBER']
    for i in range(len(data['NUMBER'])):
        if i in omit_range:
            continue
        else:
            numer += data[i][flux]/(data[i][fluxerr]**2)
            denom += 1./(data[i][fluxerr]**2)
            count += 1
    #print data['NUMBER'][i]/60000.,' min'
    flux_ave = numer/denom
    #print "count = ",count
    data[flux] = data[flux]/flux_ave
    data[fluxerr] = data[fluxerr]/flux_ave
    return data

data_target=normalizeFlux(ascii.read('target.cat'),2,range(50,269))
#data_target=ascii.read('target.cat')
data_guiding=list()

#fig = plt.figure(figsize=(20,10))
for i in range(10):
    #ax = fig.add_subplot(3,4,i+1)
    data_guiding.append(normalizeFlux(ascii.read('guiding'+str(i+1)+'.cat'),2,[]))
    #print 'i = ',i
    #print data_guiding[i]['FLUX_APER_2']
    dummy = data_guiding[i]['FLUX_APER_2']
    for j in range(len(dummy)):
        if (dummy[j] > 1.03) or (dummy[j] < 0.97):
            data_guiding[i]['FLUXERR_APER_2'][j] = 1.e40
            #print data_guiding[i]['FLUX_APER_2'][j]

    #ax.errorbar(data_guiding[i]['NUMBER'],data_guiding[i]['FLUX_APER_2'],yerr=data_guiding[i]['FLUXERR_APER_2'],fmt='o')
    #ax.set_ylim([0.95,1.05])
#plt.savefig('badpoint_eliminate.png')
#plt.show()
#sys.exit()

#data_guiding.append(ascii.read('guiding'+str(i+1)+'.cat'))

data_guiding_flux_master_list=list()
data_guiding_error_master_list=list()

#for i in [0,2,3,4,5,7,8]:
#for i in [0,1,3,4,5,6]:
for i in [0,1,3,4,5]:
    #plt.plot(data_guiding[i]['NUMBER'],data_guiding[i]['FLUX_APER_2'],label='calibration'+str(i+1))
    data_guiding_flux_master_list.append(data_guiding[i]['FLUX_APER_2']/data_guiding[i]['FLUXERR_APER_2']**2)
    data_guiding_error_master_list.append(1/data_guiding[i]['FLUXERR_APER_2']**2)

data_guiding_flux_master=data_guiding_flux_master_list[0]
data_guiding_error_master=data_guiding_error_master_list[0]
#for i in [1,2,3,4,5,6]:
#for i in [1,2,3,4,5]:
for i in [1,2,3,4]:
    data_guiding_flux_master=data_guiding_flux_master+data_guiding_flux_master_list[i]
    data_guiding_error_master=data_guiding_error_master+data_guiding_error_master_list[i]
data_guiding_flux_master=data_guiding_flux_master/data_guiding_error_master
#plt.plot(data_target['NUMBER'],data_guiding_flux_master,label='calibration master')
#plt.plot(data_target['NUMBER'],data_target['FLUX_APER_2'],label='wasp-2')

transit_ratio=data_target['FLUX_APER_2']/data_guiding_flux_master

################ Let's find average of the two plateau################
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

#rerun loop to find errors
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
# Normalize?
transit_ratio = transit_ratio/r1

################## Bin it up - 5 minutes bins #####################
binWidth = 5. #mins
num_bin = int(np.ceil(max(data_target['NUMBER'])/60000./binWidth))
bindata = np.zeros([num_bin,2])
binerror = np.zeros(num_bin)
# index for transit_ratio
j = 0
for i in range(num_bin):
    num_point = 0
    while int(data_target['NUMBER'][j]/60000./binWidth) < (i+1):
        #print i,j,data_target['NUMBER'][j]/60000.
        bindata[i,1] += transit_ratio[j]
        bindata[i,0] += data_target['NUMBER'][j]/60000.
        num_point += 1
        j+=1
        if j == len(transit_ratio):
            break
    #print num_point
    bindata[i,1] = bindata[i,1]/num_point
    bindata[i,0] = bindata[i,0]/num_point

# rerun loop to get errors
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
#####################################################################
'''
# Let's normalize one last time
bindata_ave = 0.
num_point = 0
for i in range(len(bindata)):
    if (i<7) or (i>29):
        #print i
        bindata_ave += bindata[i,1]
        num_point += 1
bindata_ave = bindata_ave/float(num_point)
bindata[:,1] = bindata[:,1]/bindata_ave
print bindata_ave
'''

#plt.plot(data_target['NUMBER']/60000.,transit_ratio,'o',label='wasp-2')
#plt.plot(bindata[:,0],bindata[:,1],'o',label='wasp-2')
plt.errorbar(bindata[:,0],bindata[:,1],yerr=binerror,fmt='o',label='wasp-2')
#plt.plot(data_target['NUMBER'],data_target['FLUX_APER_2'],label='wasp-2')
#sys.exit()
plt.legend()
plt.xlabel('Time(min)')
plt.ylabel('Normalized flux ratio')
#plt.ylim([1.45,1.55])
plt.savefig('final_lightcurve.png')
plt.show()
