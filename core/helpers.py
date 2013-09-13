#http://www.easyrgb.com/
from math import sqrt, pow

def rgb_difference(rgb1, rgb2):
        
    lab1 = rgb_to_lab(hex_to_rgb(rgb1))
    lab2 = rgb_to_lab(hex_to_rgb(rgb2))
        
    return lab_difference(lab1, lab2)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))


def rgb_to_lab(inputColor):

    RGB = [0, 0, 0]

    for idx, value in enumerate(inputColor):
        value = float(value) / 255
        
        if value > 0.04045 :
            value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
        else :
            value = value / 12.92
        
        RGB[idx] = value * 100

    XYZ = [0, 0, 0,]
    
    X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
    Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
    Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
    XYZ[ 0 ] = round( X, 4 )
    XYZ[ 1 ] = round( Y, 4 )
    XYZ[ 2 ] = round( Z, 4 )
    
    XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2, Illuminant= D65
    XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
    XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883
    
    for idx, value in enumerate(XYZ) :

        if value > 0.008856 :
            value = value ** ( 0.3333333333333333 )
        else :
            value = ( 7.787 * value ) + ( 16 / 116 )
        
        XYZ[idx] = value

    Lab = [0, 0, 0]
    
    L = ( 116 * XYZ[ 1 ] ) - 16
    a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
    b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )
    
    Lab [ 0 ] = round( L, 4 )
    Lab [ 1 ] = round( a, 4 )
    Lab [ 2 ] = round( b, 4 )
    
    return Lab


def lab_difference(lab1, lab2):
    KL = 1
    K1 = 0.045
    K2 = 0.015
    
    dL = lab1[0] - lab2[0]
    c1 = sqrt((pow(lab1[1],2) + pow(lab1[2],2)))
    c2 = sqrt((pow(lab2[1],2) + pow(lab2[2],2)))
    dC = c1 - c2
    
    da = lab1[1] - lab2[1]
    db = lab1[2] - lab2[2]
    
    tmp = pow(da, 2) + pow(db,2) - pow(dC,2)
    tmp = max(0, tmp)
    dH = sqrt(tmp)
    
    sec1 = pow((dL/KL), 2)
    sec2 = pow((dC / (1 + (K1 * c1))), 2)
    sec3 = pow((dH / (1 + (K2 * c1))), 2)
    
    return sqrt(sec1 + sec2 + sec3)