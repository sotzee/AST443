# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from astropy.io import ascii
import numpy as np

def findstar(data,table,radec,i):
    ra=list(data['ALPHA_J2000'])
    dec=list(data['DELTA_J2000'])
    tmp=list((np.array(ra)-radec[0])**2+(np.array(dec)-radec[1])**2)
    num=tmp.index(np.min(np.array(tmp)))
    table.add_row(data[num])
    table[i]['NUMBER']=35428.18568*i

target_ra=307.725
target_dec=6.4293
guiding_ra=[307.74102,307.71561,307.77097,307.68226,307.74098,307.8094,307.84249,307.83878,307.86358,307.86054]
guiding_dec=[6.4779257,6.46703,6.4522199,6.4261293,6.3633343,6.4556595,6.441245,6.471166,6.460233,6.4053414]
beginnum=33
num=408
sciencefilelist=list()
for i in range(num):
    if(i+beginnum<100):
        sciencefilelist.append('processed_flat.000000'+str(beginnum+i)+'.FIT_clean.new+.cat')
    if(i+beginnum>=100):
        sciencefilelist.append('processed_flat.00000'+str(beginnum+i)+'.FIT_clean.new+.cat')

table_target=ascii.read('blank.cat')
table_guiding=[ascii.read('blank1.cat'),ascii.read('blank2.cat'),ascii.read('blank3.cat'),ascii.read('blank4.cat'),ascii.read('blank5.cat'),ascii.read('blank6.cat'),ascii.read('blank7.cat'),ascii.read('blank8.cat'),ascii.read('blank9.cat'),ascii.read('blank10.cat')]
table_target.remove_rows(0)
for i in range(10):
    table_guiding[i].remove_rows(0)

for i in range(num):
    data=ascii.read(sciencefilelist[i])
    findstar(data,table_target,[target_ra,target_dec],i)
    for ii in range(10):
        findstar(data,table_guiding[ii],[guiding_ra[ii],guiding_dec[ii]],i)

ascii.write(table_target, 'target.cat')
for i in range(10):
    ascii.write(table_guiding[i], 'guiding'+str(i+1)+'.cat')
