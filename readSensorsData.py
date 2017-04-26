'''
Created on 26 Apr 2017

@author: T
'''
import csv
from coordConversions_Func import LonLatToUTM
import matplotlib.pyplot as plt

def readAndroSensor(fileToRead, sensorColumn = 12):
    ''' Reads data from Andro sensor in csv file
    
    :param arg1: file name or path to read
    :param arg2: number representing column used for the sensor
    :type arg1: string
    :type arg1: int starting from 0
    :return: lists of latit, longit, easting, northing, sensor
    :rtype: [float,], [float,], [float,], [float,], [float,]
    '''
    with open(fileToRead) as csvfile:
        sensorReader = csv.reader(csvfile, delimiter=',')
        
        coord = []      # hold coordinates as tuple
        easting = []    # hold empty list for easting after conversion
        northing = []   # hold empty list for northing after conversion
        sensor = []      # hold empty list for sensor data
        
        next(sensorReader) # skip the first row
        
        for row in sensorReader:  # iterate over each row and append lists
            coord.append((float(row[23]),float(row[22])))
            utmCoord = LonLatToUTM(float(row[22]), float(row[23]))
            easting.append(utmCoord[1])
            northing.append(utmCoord[2])
            sensor.append(row[sensorColumn])

    return coord, easting, northing, sensor
        
def plotPath(easting, northing):
    ''' basic plot for path '''
    plt.figure()
    plt.plot(easting, northing, label='path')
    plt.axis('equal')
    plt.xlabel('Easting [m]')
    plt.ylabel('Northing [m]')
    plt.legend()
    plt.title('Path from Uni to ThinqTanq')   
    
def plotSensor(sensor):
    ''' basic sensor plot '''
    plt.figure()
    plt.plot(sensor, label='light')
    plt.xlabel('sample point')
    plt.ylabel('Light [Lux]')
    plt.title('Light along the path')
    
if __name__ == '__main__':
    file = 'Uni2ThinqTanq.csv'
    coord, easting, northing, light = readAndroSensor(file)
    
    plotPath(easting, northing)
    plotSensor(light)
    
    plt.show()
    