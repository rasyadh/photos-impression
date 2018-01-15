import numpy as np
import json
from subspace import pca, project, reconstruct
from util import normalize, asRowMatrix, read_images
from visual import subplot

# set numpy array print option
np.set_printoptions(threshold=1000000)

# read image
IMAGE_PATH = '../att_faces_tes'
[X,y] = read_images(IMAGE_PATH, 10)

# Try to parse X to row matrix
rowX = asRowMatrix(X)

# perform pca
[eigenvalues, eigenvectors, mu] = pca(rowX, y)
print('Mean : ')
print(mu)
print()
print("eigenvalues : ")
print(eigenvalues)
print()
print("eigenvectors :")
print(len(eigenvectors))
print(eigenvectors.tolist())
print()

data = {}
data['feature'] = {
    'eigenvalues': eigenvalues.tolist(),
    'eigenvectors': eigenvectors.tolist()
}

with open('feature.json', 'w') as outfile:
    json.dump(data, outfile)