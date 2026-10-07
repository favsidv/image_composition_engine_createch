
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


class Invert:
    def __init__(self):
        pass

    def apply(self, base_color):
        return 1 - base_color



class Blur:
    def __init__(self, radius):
        self.radius = radius

    def apply(self, base_image):
        h, w, c = base_image.shape
        result = np.zeros_like(base_image)

        for y in range(h):
            for x in range(w):
                y_min = max(0, y - self.radius)
                y_max = min(h, y + self.radius + 1)

                x_min = max(0, x - self.radius)
                x_max = min(w, x + self.radius + 1)

                result[y, x] = np.mean ( base_image [ y_min:y_max, x_min:x_max], axis=(0, 1))

        return result



class GaussianBlur:

    def __init__(self, radius, sigma):
        self.radius = radius
        self.sigma = sigma

    def apply(self, base_image):
        size = 2 * self.radius + 1

        x = np.arange(-self.radius, self.radius + 1)
        kernel = np.exp(-(x ** 2) / (2 * self.sigma ** 2))
        kernel = kernel / np.sum(kernel)

        result = base_image.copy()

    
        for y in range(base_image.shape[0]):
            for x in range(base_image.shape[1]):
                for c in range(3):
                    values = []
                    weights = []

                    for i in range(size):
                        xx = x + i - self.radius

                        if 0 <= xx < base_image.shape[1]:
                            values.append(base_image[y, xx, c])
                            weights.append(kernel[i])

                    result[y, x, c] = np.average(values, weights=weights)

        final = result.copy()

        for y in range(base_image.shape[0]):
            for x in range(base_image.shape[1]):
                for c in range(3):
                    values = []
                    weights = []

                    for i in range(size):
                        yy = y + i - self.radius

                        if 0 <= yy < base_image.shape[0]:
                            values.append(result[yy, x, c])
                            weights.append(kernel[i])

                    final[y, x, c] = np.average(values, weights=weights)

        return final