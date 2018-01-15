import numpy as np
from subspace import pca, project, reconstruct
from util import normalize, asRowMatrix, read_images
from visual import subplot

# set numpy array print option
np.set_printoptions(threshold=1000000)

# read image
IMAGE_PATH = '../att_faces_tes'
[X,y] = read_images(IMAGE_PATH, 20)

# Try to parse X to row matrix
rowX = asRowMatrix(X)

# perform pca
[eigenvalues, eigenvectors, mu] = pca(rowX, y)
print("eigenvalues : ")
print(eigenvalues)
print()
print("eigenvectors :")
print(len(eigenvectors))
print(eigenvectors)
print()

import matplotlib.cm as cm

# turn the first (at most) 16 eigenvectors into grayscale
# images (note: eigenvectors are stored by column!)
E = []
for i in range(min(len(X), 10)):
    e = eigenvectors[:,i].reshape(X[0].shape)
    E.append(normalize(e,0,255))
# plot them and store the plot to "python_eigenfaces.png"
subplot(title="Eigenfaces AT&T Facedatabase", images=E, rows=5, cols=5, sptitle="Eigenface", colormap=cm.jet, filename="python_pca_eigenfaces.png")


# reconstruction steps
steps=[i for i in range(0, min(len(X), 100), 10)]
E = []
for i in range(min(len(steps), 10)):
    numEvs = steps[i]
    P = project(eigenvectors[:,0:numEvs], X[0].reshape(1,-1), mu)
    R = reconstruct(eigenvectors[:,0:numEvs], P, mu)
    # reshape and append to plots
    R = R.reshape(X[0].shape)
    E.append(normalize(R,0,255))
# plot them and store the plot to "python_reconstruction.pdf"
subplot(title="Reconstruction AT&T Facedatabase", images=E, rows=5, cols=5, sptitle="Eigenvectors", sptitles=steps, colormap=cm.gray, filename="python_pca_reconstruction.png")