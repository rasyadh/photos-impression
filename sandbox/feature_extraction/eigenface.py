import sys

# import numpy and matplotlib colormaps
import numpy as np
# import tinyfacerec modules
from tinyfacerec.subspace import pca
from tinyfacerec.util import normalize, asRowMatrix, read_images
from tinyfacerec.visual import subplot

# set numpy array print option
np.set_printoptions(threshold=1000000)
    
# read images
[X,y] = read_images('../att_faces')

# perform a full pca
[D, W, mu] = pca(asRowMatrix(X), y)

print()
print(D)
print()
print(len(W))

import matplotlib.cm as cm

# turn the first (at most) 16 eigenvectors into grayscale
# images (note: eigenvectors are stored by column!)
E = []
for i in range(min(len(X), 10)):
    e = W[:,i].reshape(X[0].shape)
    E.append(normalize(e,0,255))
# plot them and store the plot to "python_eigenfaces.png"
subplot(title="Eigenfaces AT&T Facedatabase", images=E, rows=4, cols=4, sptitle="Eigenface", colormap=cm.jet, filename="python_pca_eigenfaces.png")

from tinyfacerec.subspace import project, reconstruct

# reconstruction steps
steps=[i for i in range(10, min(len(X), 320), 20)]
E = []
for i in range(min(len(steps), 16)):
    numEvs = steps[i]
    P = project(W[:,0:numEvs], X[0].reshape(1,-1), mu)
    R = reconstruct(W[:,0:numEvs], P, mu)
    # reshape and append to plots
    R = R.reshape(X[0].shape)
    E.append(normalize(R,0,255))
# plot them and store the plot to "python_reconstruction.pdf"
subplot(title="Reconstruction AT&T Facedatabase", images=E, rows=4, cols=4, sptitle="Eigenvectors", sptitles=steps, colormap=cm.gray, filename="python_pca_reconstruction.png")