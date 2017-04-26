'''
Created on 26 Apr 2017
@author: T

Simple script for working with coordinates
Translate coordinates in degree decimal representation to 
degree, minutes, seconds
>>> deg_to_dms(50.084522)
[50, 5, 4.27919999999915]
>>> deg_to_dms(-5.699057)
[-5, 41, 56.60519999999934]

'''
deg = 50.084522

d = int(deg)
md = abs(deg - d) * 60
m = int(md)
sd = (md - m) * 60

print('my decimal coordinatees %f are: %i degres, %i minutes and %f seconds'%(deg, d, m, sd))
