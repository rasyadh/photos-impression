import json
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA, PCA
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
import cv2

#DATASET_FILE_PATH = '../../project/static/image/dataset/jaffe/eigenfaces_jaffe_dataset.json'
DATASET_FILE_PATH = '../../project/static/image/dataset/jaffe/feature_jaffe_dataset.json'
classifier = 'haarcascade_frontalface_default.xml'

with open(DATASET_FILE_PATH) as f:
    data = json.load(f)
    f.close()

X = data["data"]
Y = data["target"]

'''
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
print('Jumlah data training :', len(X_train))
print('Jumlah data testing :', len(X_test))
print('y data training :', y_train)
print('y data test :', y_test)
'''

image = cv2.imread('KA.SA1.33.tiff', 0)
face_cascade = cv2.CascadeClassifier(classifier)
faces = face_cascade.detectMultiScale(
    image,
    scaleFactor=1.5,
    minNeighbors=5,
    minSize=(50, 50),
    flags=cv2.CASCADE_SCALE_IMAGE
)
for (x, y, w, h) in faces:
    face = image[y : (y + h), x : (x + w)]
    face = cv2.resize(face, (50, 50))

print(face)
face = face.flatten()

X_train = X
X_test = []
X_test.append(face)
y_train = Y
y_test = [2]

n_components = 50

pca = PCA(svd_solver='randomized', n_components=n_components, whiten=True).fit(X_train)
eigenfaces = pca.components_.reshape((n_components, 50, 50))
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)
print(X_test_pca)

param_grid = {
    'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
}
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_pca, y_train)
print(clf.best_estimator_)

y_pred = clf.predict(X_test_pca)

print('Target prediksi :', y_test)
print('Hasil prediksi :', y_pred.tolist())

target_names = ['Netral', 'Bahagia', 'Sedih', 'Terkejut']
print(classification_report(y_test, y_pred, target_names=target_names))
n_classes = len(target_names)
print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))

# # Qualitative evaluation of the predictions using matplotlib
# def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
#     """Helper function to plot a gallery of portraits"""
#     plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
#     plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
#     for i in range(n_row * n_col):
#         plt.subplot(n_row, n_col, i + 1)
#         plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
#         plt.title(titles[i], size=12)
#         plt.xticks(())
#         plt.yticks(())

# # plot the result of the prediction on a portion of the test set
# def title(y_pred, y_test, target_names, i):
#     pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
#     true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
#     return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

# prediction_titles = [title(y_pred, y_test, target_names, i)
#                      for i in range(y_pred.shape[0])]

# plot_gallery(np.asarray(X_test), prediction_titles, 50, 50)

# # plot the gallery of the most significative eigenfaces
# eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
# plot_gallery(eigenfaces, eigenface_titles, 50, 50)

# plt.show()