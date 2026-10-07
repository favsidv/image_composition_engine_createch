
import numpy as np 


def difference ( base_color , blend_color) :
    return np.abs(base_color - blend_color)



def exclusion (base_color , blend_color) : 
    return (0.5 - 2*( base_color - 0.5)* ( blend_color-0.5))



def substract( base_color, blend_color) : 
    return ( base_color - blend_color)



def divide ( base_color, blend_color) :
    return ( base_color / blend_color)



