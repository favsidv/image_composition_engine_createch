
import numpy as np  # type: ignore


class Brightness : 

    def __init__(self, level): 
        self.level = level 

    def apply (self, base_color):
        return np.clip(base_color + self.level, 0,1)



class Contrast : 

    def __init__(self, level): 

        self.level = level 

    def apply(self, base_color) :

        return (base_color - 0.5)* self.level + 0.5


