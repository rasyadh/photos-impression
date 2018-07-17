import numpy as np
import cv2

class LocalBinaryPattern:
    def __init__(self, img, transformed_img):
        self.img = img
        self.transformed_img = transformed_img

    def thresholded(self, center, pixels):
        out = []
        for a in pixels:
            if a >= center:
                out.append(1)
            else:
                out.append(0)
        return out

    def get_pixel_else_0(self, l, idx, idy, default=0):
        try:
            return l[idx,idy]
        except IndexError:
            return default

    def process_lbp(self):
        for x in range(0, len(self.img)):
            for y in range(0, len(self.img[0])):
                center        = self.img[x,y]
                top_left      = self.get_pixel_else_0(self.img, x-1, y-1)
                top_up        = self.get_pixel_else_0(self.img, x, y-1)
                top_right     = self.get_pixel_else_0(self.img, x+1, y-1)
                right         = self.get_pixel_else_0(self.img, x+1, y )
                left          = self.get_pixel_else_0(self.img, x-1, y )
                bottom_left   = self.get_pixel_else_0(self.img, x-1, y+1)
                bottom_right  = self.get_pixel_else_0(self.img, x+1, y+1)
                bottom_down   = self.get_pixel_else_0(self.img, x,   y+1 )

                values = self.thresholded(center, [top_left, top_up, top_right, right, bottom_right, bottom_down, bottom_left, left])

                weights = [1, 2, 4, 8, 16, 32, 64, 128]
                res = 0
                for a in range(0, len(values)):
                    res += weights[a] * values[a]

                self.transformed_img.itemset((x,y), res)

        return self.transformed_img