import numpy as np

class Overlay : 

    def __init__(self): 
        pass
    
    
    def apply( self, base_color, blend_color): 

        return np.where(base_color <= 0.5,2 * base_color * blend_color,1 - 2 * (1 - base_color) * (1 - blend_color))




class Softlight :

    def __init__(self): 
        pass
    
    
    def apply( self, base_color, blend_color): 

        return np.where( (blend_color > 0.5)* (1- (1- base_color)*(1- (blend_color-0.5)))+(blend_color<= 0.5)*(blend_color * (blend_color + 0.5)))



class hardlight : 

    def __init__(self): 
        pass 
    
    def apply( self, base_color, blend_color): 
        return ((blend_color> 0.5) * (1 - (1- base_color) * (1-2*( blend_color -0.5))) + ( blend_color <= 0.5) * (base_color * (2* blend_color)))



class vivid_light : 

    def __init__(self):
        pass 
    
    
    def apply( self, base_color , blend_color): 

        return ((blend_color > 0.5) * (1 - (1- base_color) * (1- 2 *(blend_color-0.5))) +(blend_color <= 0.5) * (base_color * (2* blend_color)))




class linear_right : 

    def __init__(self):
        pass

    def apply ( self , base_color, blend_color): 
        return (( blend_color > 0.5) * (base_color + 2* (blend_color-0.5)) +(blend_color <= 0.5) * ( base_color + 2 *blend_color - 1))



class pin_light : 
    def __init__(self) : 
        pass

    def apply( self, base_color, blend_color): 

        return ((blend_color > 0.5) * ( np.maximun ( base_color, 2* (blend_color-0.5) )) + (blend_color <= 0.5 ) * (np.minimun ( base_color, 2 * blend_color)))



class hard_mix :

    def __init__(self): 
        pass


    def apply( self ,base_color, blend_color): 
        new_color = base_color + blend_color
        return np.where(new_color >= 1, 1, 0)

