# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 19:16:34 2016

@author: sotzee
"""
import numpy

jupiter_radius=69911000
solar_radius=695700000

r=1.289*jupiter_radius
R=1.237*solar_radius

print -2.5*numpy.log10(1-(r/R)**2)