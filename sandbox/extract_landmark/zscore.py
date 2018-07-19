from math import floor

class ZScoreNormalization:
    def __init__(self):
        return

    def float_round(self, num, places=0, direction=floor):
        return direction(num * (10 ** places)) / float(10 ** places)

    def create_mean_std(self, dataset):
        mean_std = []

        for i in range(len(dataset[0])):
            mean_std.append([0, 0])
        
        for i in range(len(dataset)):
            for j in range(len(dataset[i])):
                mean_std[j][0] = int(mean_std[j][0]) + int(dataset[i][j])

        for i in range(len(mean_std)):
            mean_std[i][0] = float_round(mean_std[i][0] / len(dataset), 3, round)

        for i in range(len(dataset)):
            for j in range(len(dataset[i])):
                mean_std[j][1] = int(mean_std[j][i]) + (int(dataset[i][j]) - mean_std[j][0]) ** 2
        
        for i in range(len(mean_std)):
            mean_std[i][1] = float_round(mean_std[i][1] ** (0.5), 3, round)
        
        return mean_std

    def zscore_result(self, data, mean, std):
        return float_round((data - mean) / std, 3, round)

    def zscore(self, dataset):
        new_dataset = []
        mean_std = self.create_mean_std(dataset=self.dataset)

        for i in range(len(dataset)):
            temp = []
            for j in range(len(dataset[i])):
                temp.append(zscore_result(data=dataset[i][j], mean=mean_std[j][0], std=mean_std[j][1]))
            new_dataset.append(temp)
        
        return new_dataset