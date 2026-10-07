

import random

#le pixel de sortie prend la couleur du pixel de la couche supérieure

def blend_normal(base_pixel, overlay_pixel):
    return overlay_pixel


def blend_dissolve( base_color, blend_color, opacity ) : 

     if random.random() < opacity : 
          return base_color
     else : 
          return blend_color 


def blend_behind( base_color, blend_color, alpha) :

     if alpha == 0 : 
          return blend_color 

     else : 
          return base_color


def blend_clear( base_color, blend_color ) : 
     return ( base_color[0], base_color [1], base_color[2], 0)

