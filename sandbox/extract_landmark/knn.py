from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import csv
import math

with open('fitur.csv', 'r') as f:
    reader = csv.reader(f)
    mylist = list(reader)

print(mylist)
hasil = list()
for i in range(len(mylist)):
    print(i)
    temp = []
    tmp = 0
    length = len(mylist[i]) - 1
    for j in range(length):
        print(j)
    print(mylist[i][83])