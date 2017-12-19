import numpy as np
from subspace import pca, process_pca
from util import normalize, asRowMatrix, read_images, get_face, parse_to_row_matrix
from visual import subplot

# set numpy array print option
# np.set_printoptions(threshold=100000)

# read image
IMAGE_PATH = 'data/1.pgm'
matrix = get_face(IMAGE_PATH, sz=100)

print(parse_to_row_matrix(matrix))
print()
# perform pca
[eigenvalues, eigenvectors, mean] = process_pca(parse_to_row_matrix(matrix))

#[eigenvalues, eigenvectors, mean] = pca(parse_to_row_matrix(matrix), index)

# print("eigenvalues :", eigenvalues)
# print()
# print("eigenvectors :", eigenvectors)
# print()
# print("mean :", mean)