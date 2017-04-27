'''
Created on 26 Apr 2017

@author: T
'''
import csv
from CoordConversions_Func import lon_lat_to_utm
import matplotlib.pyplot as plt

def readAndroSensor(fileToRead, sensorColumn = 12):
    ''' Reads data from Andro sensor in csv file
    
    :param arg1: file name or path to read
    :param arg2: number representing column used for the sensor
    :type arg1: string
    :type arg1: int starting from 0
    :return: lists of latit, longit, easting, northing, sensor
    :rtype: [float,], [float,], [float,], [float,], [float,]
    
    Data from sensors:
    0: ACCELEROMETER X (m/s2) 
    1: ACCELEROMETER Y (m/s2) 
    2: ACCELEROMETER Z (m/s2)   
    12: LIGHT (lux)    
    13: MAGNETIC FIELD X (uT)    
    14: MAGNETIC FIELD Y (uT)    
    15: MAGNETIC FIELD Z (uT)    
    16: ORIENTATION Z (azimuth degrees)    
    17: ORIENTATION X (pitch degrees)    
    18: ORIENTATION Y (roll degrees)    
    19: PROXIMITY (m)    
    20: ATMOSPHERIC PRESSURE (hPa)    
    21: SOUND LEVEL (dB)    
    22: LOCATION Latitude    
    23: LOCATION Longitude 

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
            utmCoord = lon_lat_to_utm(float(row[22]), float(row[23]))
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
    plt.plot(sensor, label='senosr')
    plt.xlabel('sample point')
    plt.ylabel('Sensor reading')
    plt.title('Sensor reading along the path')
    
if __name__ == '__main__':
    file = 'Uni2ThinqTanq.csv'
#    file = 'Sensor_record_20170426_194909_AndroSensor.csv'
    coord, easting, northing, sensor = readAndroSensor(file, 20)
    
    plotPath(easting, northing)
    plotSensor(sensor)
    
    plt.show()
    
