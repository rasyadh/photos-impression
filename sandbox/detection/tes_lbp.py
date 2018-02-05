import cv2
import numpy as np
from lbp import LocalBinaryPattern

img = cv2.imread('KA.HA1.29.tiff', 0)
transformed_img = cv2.imread('KA.HA1.29.tiff', 0)

lbp = LocalBinaryPattern(img, transformed_img)
result = lbp.process_lbp()
print(result)

cv2.imshow('image', img)
cv2.imshow('result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()