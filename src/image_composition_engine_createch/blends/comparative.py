
import numpy as np 


class difference : 
    def __init__(self) : 
        pass 


    def apply (self, base_color , blend_color) :
        return np.abs(base_color - blend_color)

class exclusion : 

    def __init__(self): 
        pass

    def apply ( self , base_color , blend_color) : 
        return (0.5 - 2*( base_color - 0.5)* ( blend_color-0.5))



class substract : 

    def __init__(self):
        pass
    
    def apply( self, base_color, blend_color) : 
        return np.clip( base_color - blend_color, 0, 1)



class divide : 

    def __init__(self): 
        pass 

    def apply ( self, base_color, blend_color) :
        return np.clip( base_color / blend_color , 0, 1)



