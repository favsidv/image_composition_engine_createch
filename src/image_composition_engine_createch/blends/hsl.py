import numpy as np


def rgb_to_hsl(rgb):
    r, g, b = rgb

    max_value = np.max(rgb)
    min_value = np.min(rgb)

    lightness = (max_value + min_value) / 2

    if max_value == min_value:
        hue = 0
        saturation = 0
    else:
        difference = max_value - min_value

        if lightness <= 0.5:
            saturation = difference / (max_value + min_value)
        else:
            saturation = difference / (2 - max_value - min_value)

        if max_value == r:
            hue = (g - b) / difference
        elif max_value == g:
            hue = 2 + (b - r) / difference
        else:
            hue = 4 + (r - g) / difference

        hue *= np.pi / 3

        if hue < 0:
            hue += 2 * np.pi

    return np.array([hue, saturation, lightness])


def hue(base_color , blend_color): 
    



def hsl_to_rgb(hsl):
    h, s, l = hsl

    if s == 0:
        return np.array([l, l, l])

    if l <= 0.5:
        q = l * (1 + s)
    else:
        q = l + s - l * s

    p = 2 * l - q

    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 2 * np.pi

        if t > 2 * np.pi:
            t -= 2 * np.pi

        if t < np.pi / 3:
            return p + (q - p) * 3 * t / np.pi

        if t < np.pi:
            return q

        if t < 4 * np.pi / 3:
            return p + (q - p) * 3 * (4 * np.pi / 3 - t) / np.pi

        return p

    r = hue_to_rgb(p, q, h + 2 * np.pi / 3)
    g = hue_to_rgb(p, q, h)
    b = hue_to_rgb(p, q, h - 2 * np.pi / 3)

    return np.array([r, g, b])