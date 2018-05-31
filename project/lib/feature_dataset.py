import json

class FeatureDataset:
    def _init_(self):
        return

    def get_feature_jaffe(self, DATASET_PATH, FILE_PATH, size):
        with open(FILE_PATH) as dataset:
            jaffe_data = json.load(dataset)
            dataset.close()

        feature, target, classes = [], [], []
        for index in jaffe_data:
            for image in jaffe_data[index]:
                face = None
                face = self.get_faces(image['url'], size)
                face = face.flatten()

                feature.append(face.tolist())
                target.append(image['id_expression'])

            classes.append(index)

        dataset = {
            'data': feature,
            'target': target,
            'classes': classes,
            'shape': size
        }

        with open(DATASET_PATH + 'feature_jaffe_dataset.json', 'w') as outfile:
            json.dump(dataset, outfile)
            outfile.close()

    def read_jaffe_dataset(self, DATASET_PATH):
        FILE_PATH = DATASET_PATH + 'dataset_jaffe.json'
        result, data = {}, []

        try:
            for dirname, dirnames, filenames in os.walk(DATASET_PATH):
                for subdirname in dirnames:
                    subject_path = os.path.join(dirname, subdirname)
                    for filename in os.listdir(subject_path):
                        if subdirname == 'HA':
                            id_expression = 0
                        elif subdirname == 'NE':
                            id_expression = 1
                        elif subdirname == 'SA':
                            id_expression = 2
                        elif subdirname == 'SU':
                            id_expression = 3

                        temp = {}
                        temp = {
                            'name': filename,
                            'url': 'project/static/image/dataset/jaffe/' + subdirname + '/' + filename,
                            'id_expression': id_expression
                        }

                        data.append(temp)
                        
                    result[subdirname] = data
                    data = []
        except Exception as e:
            print('error at read_jaffe_dataset in utils')
            print(e)

        with open(FILE_PATH, 'w') as outfile:
            json.dump(result, outfile)
            outfile.close()

        self.get_feature_jaffe(DATASET_PATH, FILE_PATH, 50)