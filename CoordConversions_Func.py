'''
Created on 26 Apr 2017

@author: Tomasz
Collection of conversion functions
'''
import utm
from utm.error import OutOfRangeError
import math 

#------------------------------------------------------------------------------ 
# CHALLANGE:
# finish the function which takes input in the form: 
# ThinqTanq_DegMinSec = "50 22'9.6\"N, 4 8'20.8\"W"

# def degDecMinToDegfFull(positionDecimal):
#     '''
#     function takes position represented in degrees with minutes in decimal 
#     notation
#     returns position with degrees minutes seconds notation 
#     >>> degrDecToDegfFull("50 22'9.6\"N, 4 8'20.8\"W")     
#     50.369334, -4.139102
#     '''
#     positionFull = []
#     return positionFull

def deg_to_dms(deg):
    '''Translate coordinates in degree decimal representation to 
    degree, minutes, seconds
    >>> deg_to_dms(50.084522)
    [50, 5, 4.27919999999915]
    >>> deg_to_dms(-5.699057)
    [-5, 41, 56.60519999999934]
    '''
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def degMinDecToFullDec(position):
    ''' function converts coordinate from degrees and minutes to decimal degree
    >>> pos = '50 05.0713061 N'
    >>> degMinDecToFullDec(pos)
    50.08452177
    >>> degMinDecToFullDec('005 41.9434092 W')
    -5.69905682
    >>> degMinDecToFullDec('50 05.0713061 N')
    50.08452177
    >>> degMinDecToFullDec('55;18.7116860N')
    55.31186143
    >>> degMinDecToFullDec('5023.1994,N')
    50.38665667
    >>> degMinDecToFullDec('00408.6421,W')
    -4.144035
    >>> degMinDecToFullDec('5023.1994,S')
    -50.38665667
    >>> degMinDecToFullDec('00408.6421,E')
    4.144035
    ''' 
    if " " in position:
        l = position.split(" ")
#        print l 
        deg = int(l[0])
        minut = float(l[1])
#        print deg, minunt
        if l[-1] in ['S', 'W']:
            sph = -1
        else:
            sph = 1
    elif ";" in position:
        l = position.split(";")
#        print l 
        deg = int(l[0])
        minut = float(l[1][0:-1])
#        print deg, minut
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
    coord = '%.8f' % ((deg + minut/60)*sph)      
    return float(coord)

def LonLatToUTM(Lat, Long):
    ''' Function converts from any [Lat, Long] to [East, North, Grid]
    >>> LonLatToUTM(50.084522, -5.699057)
    ['30U 306918.367 5551517.614', 306918.367, 5551517.614]
    >>> LonLatToUTM('50 05.0713061 N', '005 41.9434092 W')
    ['30U 306918.379 5551517.588', 306918.379, 5551517.588]
    >>> LonLatToUTM(50.0845217683, -5.69905682)
    ['30U 306918.379 5551517.588', 306918.379, 5551517.588]
    
    '''
    # Check if Lat and Long already in decimal
    if type(Lat)==float and type(Long)==float:
        pass
    elif type(Lat)==str and type(Long)==str:
        Lat = degMinDecToFullDec(Lat)
        Long = degMinDecToFullDec(Long)
    # Check if correct range    
    if not -80.0 <= Lat <= 84.0:
        raise OutOfRangeError('latitude out of range (must be between 80 deg S and 84 deg N)')
    if not -180.0 <= Long <= 180.0:
        raise OutOfRangeError('northing out of range (must be between 180 deg W and 180 deg E)')

    utmPos = utm.from_latlon(Lat, Long)
#    print('my utm postition from the function: {} with Lat: {} and Long: {} as input'.format(utmPos, Lat, Long))   
    # Google Earth does not accept this format. Translation for Google Earth:
    East = '%.3f' % (utmPos[0])
    North = '%.3f' % (utmPos[1])
    Grid1 = str(utmPos[2])
    Grid2 = str(utmPos[3])
    GooglEarth = (Grid1 + Grid2+' '+East+' '+North) 
    
    # returns Google Earth format and Easting and Northind as float
    return [GooglEarth, float(East), float(North)]

#------------------------------------------------------------------------------ 
# CALCULATING DISTANCE 

def checkDistanceShort(UTM_firstPos, UTM_secondPos):
    ''' check straigth line distance between two points
    it is possible but unreadable'''
    return ((UTM_firstPos[0]-UTM_secondPos[0])**2+(UTM_firstPos[1]-UTM_secondPos[1])**2)**(0.5)

def checkDistance(UTM_firstPos, UTM_secondPos):
    ''' better function
    check straigth line distance between two points
    
    :param arg1: Easting and Northing of the first position
    :param arg2: Easting and Northing of the second position
    :type arg1: tuple (Easting, Northing)
    :type arg1: tuple (Easting, Northing)
    :return: return distance in metres
    :rtype: float
    '''
    try:
        # x,y coordinates of the first point
        xPos1 = UTM_firstPos[0]
        yPos1 = UTM_firstPos[1]
        # x,y coordinates of the second point
        xPos2 = UTM_secondPos[0]
        yPos2 = UTM_secondPos[1]
        # cartesian distance
        distance = math.sqrt((xPos1-xPos2)**2 + (yPos1-yPos2)**2)
        
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

    LatDecimal = degMinDecToFullDec(Latit +','+ LatitHem)
    LongDecimal = degMinDecToFullDec(Longit +','+ LongitHem)
    
    # check what you've got:
    print(' after converstion Latitude: {} of type: {}, Longitude: {} of type: {}'.
          format(LatDecimal, type(LatDecimal), LongDecimal, type(LongDecimal)))
    
    return  LonLatToUTM(LatDecimal, LongDecimal)

if __name__ == '__main__':

    # ThinqTanq position:
    ThinqTanq_Decimal = [50.369334, -4.139102]
    ThinqTanq_UTM = '30U 418991.987 5580316.488'
    
    uni_Deg = ('50 22.502209 N', '004 08.329597 W')

    uni_decimal = (degMinDecToFullDec(uni_Deg[0]), degMinDecToFullDec(uni_Deg[1]))
    print('check in map: ', uni_decimal)
      
    Latit = ThinqTanq_Decimal[0]
    Longit = ThinqTanq_Decimal[1]
    utmTT = LonLatToUTM(Latit, Longit)
    utmUni = LonLatToUTM(uni_decimal[0], uni_decimal[1])
 
    print('utmThinqTanq = %s' % str(utmTT))
    print(deg_to_dms(Latit))
    print(deg_to_dms(Longit))    
    
    print('utmUni = {}'.format(utmUni))
    
    print((utmUni[1], utmUni[2]), (utmTT[1],utmTT[2]))
    distUniTinqTanq = checkDistance((utmUni[1], utmUni[2]), (utmTT[1],utmTT[2]))
    print('distance between Uni and ThinqTanq = {}'.format(distUniTinqTanq))
    
    print(customCoordTranslate("5022.502209,N,00408.329597,W"))
    
#     import doctest
#     doctest.testmod()
    