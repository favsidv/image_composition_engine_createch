import numpy as np

def contrast_overlay( base_color, blend_color): 

    return np.where(base_color <= 0.5,2 * base_color * blend_color,1 - 2 * (1 - base_color) * (1 - blend_color))



def contrast_softlight( base_color, blend_color): 

    return np.where( (blend_color > 0.5)* (1- (1- base_color)*(1- (blend_color-0.5)))+(blend_color<= 0.5)*(blend_color * (blend_color + 0.5)))




def contrast_hardlight(base_color, blend_color): 
    return ((blend_color> 0.5) * (1 - (1- base_color) * (1-2*( blend_color -0.5))) + ( blend_color <= 0.5) * (base_color * (2* blend_color)))




def contrast_vividlight( base_color , blend_color): 

    return ((blend_color > 0.5) * (1 - (1- base_color) * (1- 2 (blend_color-0.5))) +(blend_color <= 0.5) * (base_color * (2* blend_color)))


 