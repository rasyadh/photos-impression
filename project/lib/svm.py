from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

class SupportVectorMachine:
    def __init__(self):
        return

    def train(self, data, label):
        print("fitting the classifier to the training set")

        param_grid = {
            'C': [1e3, 5e3, 1e4, 5e4, 1e5],
            'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
        }
        
        clf = GridSearchCV(SVC(
            kernel='rbf', class_weight='balanced'), param_grid)
        #clf = clf.fit(data['eigenvectors'], data['label'])
        clf = clf.fit(data, label)

        print("Best estimator found by grid search:")
        print(clf.best_estimator_)

        return clf

    def predict(self, clf, data_test):
        print("predictiong expression names on the test set")
        label_pred = clf.predict(data_test)

        return label_pred