import numpy as np 



class Lighten : 

    def __init__(self) : 
        pass

    def apply( self, base_color, blend_color) :
        return np.maximun(base_color, blend_color)




class screen : 
    def __init__(self): 
        pass

    def apply( self, base_color , blend_color): 
        return (1 - (1-base_color) * (1-blend_color))



class color_dodge : 
    def __init__(self): 
        pass
    
    
    def apply( self, base_color, blend_color): 
        return (base_color / (1- blend_color))



class linear_dodge : 

    def __init__(self):
        pass
    
    def apply( self, base_color, blend_color) :
        return base_color + blend_color




class lighter_color : 

    def __init__(self) :
        pass 
    
    def apply ( self, base_color, blend_color) : 
        total_base = np.sum ( base_color )
        total_blend = np.sum( blend_color)
        if total_base >  total_blend : 
            return base_color
        else : 
            return blend_color