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
    print data['NUMBER'][i]/60000.,' min'
    flux_ave = numer/denom
    print "count = ",count
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
    print 'i = ',i
    #print data_guiding[i]['FLUX_APER_2']
    dummy = data_guiding[i]['FLUX_APER_2']
    for j in range(len(dummy)):
        if (dummy[j] > 1.02) or (dummy[j] < 0.98):
            data_guiding[i]['FLUXERR_APER_2'][j] = 1.e40

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

########### Let's average one more time - unweighted
print len(transit_ratio)
'''
ratio_ave = transit_ratio.sum()/len(transit_ratio)
for i in range(len(transit_ratio)):
    transit_ratio[i] = transit_ratio[i]/ratio_ave
'''
### Bin it up - 5 minutes bins
binWidth = 2. #mins
num_bin = int(np.ceil(max(data_target['NUMBER'])/60000./binWidth))-1
bindata = np.zeros(num_bin)
# index for transit_ratio
j = 0
for i in range(num_bin):
    num_point = 0
    while int(data_target['NUMBER'][j]/60000./binWidth) < (i+1):
        print i,j,data_target['NUMBER'][j]/60000.
        bindata[i] += transit_ratio[j]
        num_point += 1
        j+=1
        if j == len(transit_ratio):
            break
    print num_point
    bindata[i] = bindata[i]/num_point
print bindata
print np.array(range(num_bin))*binWidth+binWidth/2.
#plt.plot(data_target['NUMBER'],transit_ratio,'o',label='wasp-2')
plt.plot(np.array(range(num_bin))*5.+2.5,bindata,'o',label='wasp-2')
#plt.plot(data_target['NUMBER'],data_target['FLUX_APER_2'],label='wasp-2')
#sys.exit()
plt.legend()
plt.xlabel('time')
plt.ylabel('ratio')
#plt.ylim([1.45,1.55])
#plt.savefig('guiding_newbest_elimbad_ave.png')
plt.show()
