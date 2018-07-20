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

DATASET_FILE_PATH = '../../../project/static/image/dataset/jaffe/feature_jaffe_dataset.json'
DATASET_INDO_PATH = '../../../project/static/image/dataset/indonesia/feature_indonesia_dataset.json'
classifier = '../haarcascade_frontalface_default.xml'

with open(DATASET_FILE_PATH) as f:
    data = json.load(f)
    f.close()

X_train = data["data"]
y_train = data["target"]

with open(DATASET_INDO_PATH) as f:
    data = json.load(f)
    f.close()

X_test = [
    data["data"][0], data["data"][1],
    data["data"][10], data["data"][11],
    data["data"][20], data["data"][21],
    data["data"][30], data["data"][31]
]
y_test = [1, 1, 0, 0, 2, 2, 3, 3]

n_components = 100
pca = PCA(svd_solver='randomized', n_components=n_components, whiten=True).fit(X_train)
eigenfaces = pca.components_.reshape((n_components, 120, 120))
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

param_grid = {
    'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
}
clf = GridSearchCV(SVC(kernel='linear', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_pca, y_train)
print(clf.best_estimator_)

y_pred = clf.predict(X_test_pca)

print()
print('Target prediksi :', y_test)
print('Hasil prediksi :', y_pred.tolist())
print()

target_names = ['Netral', 'Bahagia', 'Sedih', 'Terkejut']
print(classification_report(y_test, y_pred, target_names=target_names))
n_classes = len(target_names)
print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))

# Qualitative evaluation of the predictions using matplotlib
def plot_gallery(images, titles, h, w, n_row=2, n_col=4):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())

# plot the result of the prediction on a portion of the test set
def title(y_pred, y_test, target_names, i):
    pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
    return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

prediction_titles = [title(y_pred, y_test, target_names, i)
                     for i in range(y_pred.shape[0])]

plot_gallery(np.asarray(X_test), prediction_titles, 120, 120)

plt.show()