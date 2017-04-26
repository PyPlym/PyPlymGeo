'''
Created on 26 Apr 2017

@author: T
'''
import csv
from CoordConversions_Func import LonLatToUTM
import matplotlib.pyplot as plt

def readAndroSensor(fileToRead, sensorColumn = 12):
    with open(fileToRead) as csvfile:
        sensorReader = csv.reader(csvfile, delimiter=',')
        
        latit = []      # hold empty list for latitude
        longit = []     # hold empty list for longitude
        easting = []    # hold empty list for easting after conversion
        northing = []   # hold empty list for northing after conversion
        sensor = []      # hold empty list for sensor data
        
        next(sensorReader) # skip the first row
        for row in sensorReader:  
            latit.append(float(row[22]))
            longit.append(float(row[23]))
            utmCoord = LonLatToUTM(float(row[22]), float(row[23]))
            easting.append(utmCoord[1])
            northing.append(utmCoord[2])
            sensor.append(row[sensorColumn])

    return latit, longit, easting, northing, sensor
            
            
        
def plotPath(easting, northing):
    plt.figure()
    plt.plot(easting, northing, label='path')
    plt.axis('equal')
    plt.xlabel('Easting [m]')
    plt.ylabel('Northing [m]')
    plt.legend()
    plt.title('Path from Uni to ThinqTanq')   
    
def plotSensor(sensor):
    plt.figure()
    plt.plot(sensor, label='light')
    plt.xlabel('sample point')
    plt.ylabel('Light [Lux]')
    plt.title('Light along the path')
    
if __name__ == '__main__':
    file = 'Uni2ThinqTanq.csv'
    latitude, longitude, easting, northing, light = readAndroSensor(file)
    print(easting)
    print(northing)
    
    plotPath(easting, northing)
    plotSensor(light)
    
    plt.show()
    