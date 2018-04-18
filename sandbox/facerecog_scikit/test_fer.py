import json
from time import time

import numpy as np
import cv2

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import PCA
from sklearn.svm import SVC

CASECADE_CLASSIFIER_PATH = "cascade/haarcascade_frontalface_default.xml"

img = cv2.imread('tes2.jpeg', 0)

detector = cv2.CascadeClassifier(CASECADE_CLASSIFIER_PATH)
faces = detector.detectMultiScale(
    img,
    scaleFactor=1.5,
    minNeighbors=5,
    minSize=(50, 50),
    flags=cv2.CASCADE_SCALE_IMAGE
) 

for (x, y, w, h) in faces:
    face = img[y : (y + h), x : (x + w)]
    face = cv2.resize(face, (30, 30))

X_test = []
X_test.append(face.flatten())

with open('feature_dataset.json') as dataset:
    jaffe_data = json.load(dataset)
    dataset.close()

X = np.asarray(jaffe_data['data'])
y = np.asarray(jaffe_data['target'])

n_samples = len(X)
n_features = len(X[0])
n_classes = len(jaffe_data['classes'])

print('y: ')
print(y)

target_names = ['HA', 'NE', 'SA', 'SU']
target_names = np.asarray(target_names)
print('target_names: ')
print(target_names)

print("Total dataset size:")
print("n_samples: %d" % n_samples)
print("n_features: %d" % n_features)
print("n_classes: %d" % n_classes)

X_train = X
y_train = y

# Compute a PCA (eigenface) on the face dataset
n_components = 50

print("Extraction the top %d eigenfaces from %d faces" % (n_components, X_train.shape[0]))
t0 = time()
pca = PCA(svd_solver='randomized', n_components=n_components, whiten=True).fit(X_train)
print("done in %0.3fs" % (time() - t0))

eigenfaces = pca.components_.reshape((n_components, 30, 30))

print("Projecting the input data on the eigenfaces orhonormal basis")
t0 = time()
X_train_pca = pca.transform(X_train)

X_test_pca = pca.transform(X_test)
print("done in %0.3fs" % (time() - t0))

print(len(X_train_pca), len(X_train_pca[0]))

# Train a SVM classification model
print("fitting the classifier to the training set")
t0 = time()
param_grid = {
    'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
}
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_pca, y_train)
print("done in %0.3fs" % (time() - t0))
print("Best estimator found by grid search:")
print(clf.best_estimator_)

# Quantitative evaluation of the model quality on the test set
print("Predictiong people's names on the test set")
t0 = time()
y_pred = clf.predict(X_test_pca)
print("done in %0.3fs" % (time() - t0))

print(y_pred)