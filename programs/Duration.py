# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 18:02:46 2016

@author: sotzee
"""

solar_mass=1.989*10**30
solar_radius=695700000
G=6.67408*10**-11
AU=1.4960*10**11
JD=24*60*60

M=1.218*solar_mass
R=1.237*solar_radius
d=0.0413*AU
T=2.77596*JD

v=(M*G/d)**0.5
print 2*R/v/60/60
v=(2*3.1415*M*G/T)**(1.0/3.0)
print 2*R/v/60/60