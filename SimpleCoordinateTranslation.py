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
deg_dec = 50.084522

degrees = int(deg_dec)
minutes_dec = abs(deg_dec - degrees) * 60
minutes = int(minutes_dec)
seconds = (minutes_dec - minutes) * 60

print('my decimal coordinatees %f are: %i degres, %i minutes and %f seconds'%(deg_dec, degrees, minutes, seconds))
