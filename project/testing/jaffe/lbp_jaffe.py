import cv2
import numpy as np
import json
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC, LinearSVC
import matplotlib.pyplot as plt
from lbp import LocalBinaryPatterns

DATASET_FILE_PATH = '../../../project/static/image/dataset/jaffe/dataset_jaffe.json'

with open(DATASET_FILE_PATH) as f:
    data = json.load(f)
    f.close()

def get_faces(img):
    face = None
    classifier = '../haarcascade_frontalface_default.xml'
    # read image data
    image = cv2.imread('../../../' + img, 0)
    # set cascade classifier 
    face_cascade = cv2.CascadeClassifier(classifier)
    # detect faces in image
    faces = face_cascade.detectMultiScale(
        image,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # get face area only
    for (x, y, w, h) in faces:
        # default face dimension 182x182
        face = image[y : (y + h), x : (x + w)]
        
        # resize image
        face = cv2.resize(face, (120, 120))

    return face

# LBP
desc = LocalBinaryPatterns(24, 8)
feature, target, classes = [], [], []
for index in data:
    for image in data[index]:
        face = None
        face = get_faces(image['url'])

        hist = desc.describe(face)
        
        feature.append(hist)
        
        target.append(image['id_expression'])

    classes.append(index)

X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size=0.25)
print('Jumlah data training :', len(X_train))
print('Jumlah data testing :', len(X_test))
print('y data training :', y_train)
print('y data test :', y_test)


# SVM
param_grid = {
    'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
}
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
clf = clf.fit(X_train, y_train)
print(clf.best_estimator_)

'''
model = LinearSVC(
    C=100.0,
    random_state=42
)
clf = model.fit(X_train, y_train)
'''

y_pred = []
for data_test in X_test:
    prediction = clf.predict(data_test.reshape(1, -1))
    y_pred.append(prediction[0])

print()
print('Target prediksi :', y_test)
print('Hasil prediksi :', y_pred)
print()

target_names = ['Netral', 'Bahagia', 'Sedih', 'Terkejut']
print(classification_report(y_test, y_pred, target_names=target_names))
n_classes = len(target_names)
print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))