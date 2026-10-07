
import numpy as np

class Darken : 

    def __init__(self):
        pass

    def apply( self, base_color, blend_color): 

        minR = min( base_color[0], blend_color[0])
        minG = min(base_color[1], blend_color[1])
        minB = min(base_color[2], blend_color[2])

        return (minR, minG, minB)



class multiply : 

    def __init__(self) : 
        pass    

    def apply(self, base_color, blend_color):

        return (base_color * blend_color)




class color_burn :

    def __init__(self): 
        pass

    def apply( self, base_color, blend_color): 

        formula = 1 - ((1-base_color)/blend_color)
        return formula




class linear_burn : 

    def __init__(self):
        pass



    def apply( self, base_color, blend_color): 

        formula2 = base_color + blend_color -1
        return formula2



class darker_color : 

    def __init__(self): 
        pass

    def apply( self, base_color, blend_color): 

        total_base = np.sum(base_color)
        total_blend = np.sum( blend_color)

        if total_base < total_blend : 
            return base_color
        else : 
            return blend_color

    