'''
Created on 26 Apr 2017

@author: T

The script converts data to a file for Google Earth
One of many modules dealing with coordinates conversion
http://simplekml.readthedocs.io/en/latest/index.html
'''
import simplekml   # if not installed: pip install simplekml
from readSensorsData import readAndroSensor

file = 'Uni2ThinqTanq.csv'
coord, easting, northing, light = readAndroSensor(file)

kml = simplekml.Kml()

ls = kml.newlinestring(name='path Uni to TT')
ls.coords = coord
ls.extrude = 1
ls.altitudemode = simplekml.AltitudeMode.relativetoground
ls.style.linestyle.width = 5
ls.style.linestyle.color = light #simplekml.Color.blue
kml.save("LineString Styling.kml")

    