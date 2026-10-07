import numpy as np 


def lighten( base_color, blend_color) :
    return np.max(base_color, blend_color)


def screen( base_color , blend_color): 
    return (1 - (1-base_color) * (1-blend_color))


def color_dodge( base_color, blend_color): 
    return (base_color / (1- blend_color))


def linear_dodge( base_color, blend_color) :
    return base_color + blend_color


def lighter_color (base_color, blend_color) : 
    total_base = np.sum ( base_color )
    total_blend = np.sum( blend_color)
    if total_base >  total_blend : 
        return base_color
    else : 
        return blend_color