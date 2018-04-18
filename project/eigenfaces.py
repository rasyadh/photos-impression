import json
import numpy as np
from time import time

from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import PCA

class Eigenfaces:
    def __init__(self, n_components):
        self.n_components = n_components

    def prepare_data(self, FILE_PATH):
        with open(FILE_PATH) as feature_data:
            feature_jaffe = json.load(feature_data)
            feature_data.close()

        datas = {
            'data': np.asarray(feature_jaffe['data']),
            'label': feature_jaffe['target'],
            'target_names': np.asarray(feature_jaffe['classes']),
            'shape': feature_jaffe['shape'],
            'n_samples': len(feature_jaffe['data']),
            'n_features': len(feature_jaffe['data'][0]),
            'n_classes': len(feature_jaffe['classes'])
        }

        return datas

    def principle_component_analysis(self, datas):
        print("extraction the top %d eigenfaces from %d faces" % (self.n_components, datas['data'].shape[0]))

        pca = PCA(
            svd_solver='randomized',
            n_components=self.n_components,
            whiten=True,
        ).fit(datas['data'])

        eigenfaces = pca.components_.reshape((
            self.n_components, datas['shape'], datas['shape']
        ))

        print("projecting the input data on the eigenfaces orhonormal basis")

        data = pca.transform(datas['data'])

        return data

    def pca_data_test(self, dataset):
        pca = PCA(
            svd_solver='randomized',
            n_components=self.n_components,
            whiten=True,
        ).fit(dataset['data'])

        eigenfaces = pca.components_.reshape((
            self.n_components, 50, 50
        ))

        return pca