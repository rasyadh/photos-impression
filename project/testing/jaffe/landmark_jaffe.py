import json
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC, LinearSVC
import matplotlib.pyplot as plt
import numpy as np
import cv2

PHOTO_FILE_PATH = '../../../project/static/image/dataset/jaffe/dataset_jaffe.json'
with open(PHOTO_FILE_PATH) as f:
    dataset = json.load(f)
    f.close()

photos, target = [], []
for index in dataset:
    for photo in dataset[index]:
        photos.append(photo['url'])
        target.append(photo['id_expression'])

DATASET_FILE_PATH = '../../../project/static/image/dataset/jaffe/feature_landmark_jaffe_dataset.json'
with open(DATASET_FILE_PATH) as f:
    data = json.load(f)
    f.close()

X = photos
y = target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

indeks_test, indeks_train = [], []
X_train_mark, X_test_mark, y_train_mark, y_test_mark = [], [], [], []
for i in range(len(photos)):
    if photos[i] in X_test:
        indeks_test.append(i)
        X_test_mark.append(data['data'][i])
        y_test_mark.append(data['target'][i])
    else:
        indeks_train.append(i)
        X_train_mark.append(data['data'][i])
        y_train_mark.append(data['target'][i])

print('Jumlah data training :', len(X_train_mark))
print('Jumlah data testing :', len(X_test_mark))
print('y data training :', y_train_mark)
print('y data test :', y_test_mark)
print()

param_grid = {
    'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
}
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_mark, y_train_mark)
print(clf.best_estimator_)

y_pred = clf.predict(X_test_mark)

print()
print('Target prediksi :', y_test_mark)
print('Hasil prediksi :', y_pred.tolist())
print()

target_names = ['Netral', 'Bahagia', 'Sedih', 'Terkejut']
print(classification_report(y_test_mark, y_pred, target_names=target_names))
n_classes = len(target_names)
print(confusion_matrix(y_test_mark, y_pred, labels=range(n_classes)))

# Qualitative evaluation of the predictions using matplotlib
def plot_gallery(images, titles, h, w, n_row=4, n_col=7):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i], cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())

# plot the result of the prediction on a portion of the test set
def title(y_pred, y_test, target_names, i):
    pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
    return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

prediction_titles = [title(y_pred, y_test_mark, target_names, i) for i in range(y_pred.shape[0])]

photo_test = []
for i in indeks_test:
    image = cv2.imread('../../../' + photos[i], 0)
    photo_test.append(image)

plot_gallery(photo_test, prediction_titles, 120, 120)

plt.show()