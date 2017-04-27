'''
Created on 26 Apr 2017

@author: Tomasz
Collection of conversion functions
'''
import utm
from utm.error import OutOfRangeError
import math 

#------------------------------------------------------------------------------ 
# CHALLENGE:
# Finish the function which takes input in the form: 
# ThinqTanq_DegMinSec = '''50 22'9.6"N, 4 8'20.8"W'''
# (note: the string is everything between the '''s - using this notation allows
# the string to contain " and ' characters.)

# def degDecMinToDegfFull(positionDecimal):
#     '''
#     f position represented in degrees with minutes in decimal 
#     notation
#     returns position with degrees minutes seconds notation 
#     >>> degrDecToDegfFull('''50 22'9.6"N, 4 8'20.8"W''')     
#     50.369334, -4.139102
#     '''
#     positionFull = []
#     return positionFull

def dec_to_deg_min_sec(deg):
    '''Translate coordinates in degree decimal representation to 
    degree, minutes, seconds.
    Examples:
    >>> dec_to_deg_min_sec(50.084522)
    [50, 5, 4.27919999999915]
    >>> dec_to_deg_min_sec(-5.699057)
    [-5, 41, 56.60519999999934]
    '''
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def deg_min_str_to_dec(position):
    ''' Convert a coordinate from a string containing degrees and minutes to decimal degree.
    Examples:
    >>> pos = '50 05.0713061 N'
    >>> deg_min_str_to_dec(pos)
    50.08452177
    >>> deg_min_str_to_dec('005 41.9434092 W')
    -5.69905682
    >>> deg_min_str_to_dec('50 05.0713061 N')
    50.08452177
    >>> deg_min_str_to_dec('55;18.7116860N')
    55.31186143
    >>> deg_min_str_to_dec('5023.1994,N')
    50.38665667
    >>> deg_min_str_to_dec('00408.6421,W')
    -4.144035
    >>> deg_min_str_to_dec('5023.1994,S')
    -50.38665667
    >>> deg_min_str_to_dec('00408.6421,E')
    4.144035
    ''' 
    if " " in position:
        l = position.split(" ")
        deg = int(l[0])
        minut = float(l[1])
        if l[-1] in ['S', 'W']:
            sph = -1
        else:
            sph = 1
    elif ";" in position:
        l = position.split(";")
        deg = int(l[0])
        minut = float(l[1][0:-1])
        if l[-1] in ['S', 'W']:
            sph = -1
        else:
            sph = 1    
    elif ',' in position[-2]:
        if position[-1] == 'N':
            deg = int(position[0:2])
            minut = float(position[2:-2])
            sph = 1
        elif position[-1] == 'S':
            deg = int(position[0:2])
            minut = float(position[2:-2])
            sph = -1
        elif position[-1] == 'W':
            deg = int(position[0:3])
            minut = float(position[3:-2]) 
            sph = -1           
        elif position[-1] == 'E':
            deg = int(position[0:3])
            minut = float(position[3:-2])
            sph = 1
        else: 
            deg = 0
            minut = 0  
            sph = 1                                                              
    coord = ((deg + minut/60)*sph)
    return round(coord, 8)

def lon_lat_to_utm(lat, lon):
    ''' Function converts from any [Lat, Long] to [East, North, Grid]
    >>> lon_lat_to_utm(50.084522, -5.699057)
    ['30U 306918.367 5551517.614', 306918.367, 5551517.614]
    >>> lon_lat_to_utm('50 05.0713061 N', '005 41.9434092 W')
    ['30U 306918.379 5551517.588', 306918.379, 5551517.588]
    >>> lon_lat_to_utm(50.0845217683, -5.69905682)
    ['30U 306918.379 5551517.588', 306918.379, 5551517.588]
    
    '''
    # Convert from strings if required.
    if type(lat) == str:
        lat = deg_min_str_to_dec(lat)
    if type(lon) == str:
        long = deg_min_str_to_dec(lon)

    # Check if correct range    
    if not -80.0 <= lat <= 84.0:
        raise OutOfRangeError('latitude out of range (must be between 80 deg S and 84 deg N)')
    if not -180.0 <= lon <= 180.0:
        raise OutOfRangeError('longditude out of range (must be between 180 deg W and 180 deg E)')

    utm_pos = utm.from_latlon(lat, lon)
#    print('my utm postition from the function: {} with Lat: {} and Long: {} as input'.format(utmPos, Lat, Long))   
    # Google Earth does not accept this format. Translation for Google Earth:
    east = '%.3f' % (utm_pos[0])
    north = '%.3f' % (utm_pos[1])
    grid1 = str(utm_pos[2])
    grid2 = str(utm_pos[3])
    google_earth = (grid1 + grid2+' '+east+' '+north) 
    
    # returns Google Earth format and Easting and Northing as float
    return [google_earth, float(east), float(north)]

#------------------------------------------------------------------------------ 
# CALCULATING DISTANCE 

def calc_distance_short(utm_pos_1, utm_pos_2):
    ''' Calculate straight line distance between two points: works 
    but is difficult to read!'''
    return ((utm_pos_1[0]-utm_pos_2[0])**2+(utm_pos_1[1]-utm_pos_2[1])**2)**(0.5)

def calc_distance(utm_pos_1, utm_pos_2):
    ''' Easier to read function to calculate the straight line distance 
    between two points.
    
    :param arg1: Easting and Northing of the first position
    :param arg2: Easting and Northing of the second position
    :type arg1: tuple (Easting, Northing)
    :type arg1: tuple (Easting, Northing)
    :return: return distance in metres
    :rtype: float
    '''
    try:
        # x,y coordinates of the first point
        x_1 = utm_pos_1[0]
        y_1 = utm_pos_1[1]
        # x,y coordinates of the second point
        x_2 = utm_pos_2[0]
        y_2 = utm_pos_2[1]
        # cartesian distance
        distance = math.sqrt((x_1-x_2)**2 + (y_1-y_2)**2)
        
        return distance  
          
    except Exception as e: print('Check if coordinates in correct form as (Easting, Northing)\n becasue: {}'.format(e))
    
#------------------------------------------------------------------------------ 
# CUSTOM COORDINATES TRANSLATION
def customCoordTranslate(coordinate):
    ''' function reads custom string as provided by andro-Sensor .csv
    
    :param arg1: cordinates in the form "DDMM.SSS,H,DDMM,SSS,H"
    :type arg1: string
    :return: return tuple of cooridnates (Easting, Northing, grid)
    :rtype: tuple: (float, float, str)
    
    >>>customCoordTranslate("5022.502209,N,00408.329597,W")
    ['30U 419021.279 5580950.271', 419021.279, 5580950.271]
    '''
    # separate string into single entries
    coordList = coordinate.split(',')
    
    # check what you have after split
    print(coordList)

    # get each postion
    Latit = coordList[0]
    LatitHem = coordList[1]
    Longit = coordList[2]
    LongitHem = coordList[3]
    
    # make sure you ckeck what type each variable is:
    print(type(Latit), Latit, LatitHem, type(Longit), Longit, LongitHem)

    LatDecimal = deg_min_str_to_dec(Latit +','+ LatitHem)
    LongDecimal = deg_min_str_to_dec(Longit +','+ LongitHem)
    
    # check what you've got:
    print(' after converstion Latitude: {} of type: {}, Longitude: {} of type: {}'.
          format(LatDecimal, type(LatDecimal), LongDecimal, type(LongDecimal)))
    
    return  lon_lat_to_utm(LatDecimal, LongDecimal)

# This is the code that will run if you just run this file as a script (rather than
# importing it into another script.
if __name__ == '__main__':
    # ThinqTanq position:
    thinqtanq_decimal = [50.369334, -4.139102]
    #thinqtanq_utm = '30U 418991.987 5580316.488'
    
    # University position:
    uni_deg = ('50 22.502209 N', '004 08.329597 W')
    uni_decimal = (deg_min_str_to_dec(uni_deg[0]), deg_min_str_to_dec(uni_deg[1]))
    print('University position (check on map):' + str(uni_decimal))
      
    thinqtanq_lat = thinqtanq_decimal[0]
    thinqtanq_lon = thinqtanq_decimal[1]

    thinqtanq_utm = lon_lat_to_utm(thinqtanq_lat, thinqtanq_lon)
    uni_utm = lon_lat_to_utm(uni_decimal[0], uni_decimal[1])
 
    print('ThinqTanq UTM = %s' % str(thinqtanq_utm))
    #print(dec_to_deg_min_sec(thinqtanq_lat))
    #print(dec_to_deg_min_sec(thinqtanq_lon))    
    
    print('University UTM = {}'.format(uni_utm))
    
    #print((uni_utm[1], uni_utm[2]), (thinqtanq_utm[1],thinqtanq_utm[2]))
    distance = calc_distance((uni_utm[1], uni_utm[2]), 
                             (thinqtanq_utm[1],thinqtanq_utm[2]))
    print('Distance between Uni and ThinqTanq = {}'.format(distance))
    
    #print(customCoordTranslate("5022.502209,N,00408.329597,W"))
    
#     import doctest
#     doctest.testmod()
    
