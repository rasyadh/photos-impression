class Normalization:
    def __init__(self):
        self.newmaks_x = 1
        self.newmaks_y = 1
        self.newmin_x = 0
        self.newmin_y = 0
        self.minimal_y = 1000
        self.minimal_x = 1000
        self.maks_x = 0
        self.maks_y = 0

    def normalize(self, feature):
        for value in range(len(feature)):
            if value % 2 == 0:
                if feature[value] < self.minimal_x:
                    self.minimal_x = float(feature[value])
                if feature[value] > self.maks_x:
                    self.maks_x = float(feature[value])
            else:
                if feature[value] < self.minimal_y:
                    self.minimal_y = float(feature[value])
                if feature[value] > self.maks_y:
                    self.maks_y = float(feature[value])
        
        for value in range(len(feature)):
            if value % 2 == 0:
                newdata = (float(feature[value]) - self.minimal_x) * (self.newmaks_x - self.newmin_x) / (self.maks_x - self.minimal_x) + self.newmin_x
                feature[value] = newdata
            else:
                newdata = (float(feature[value]) - self.minimal_y) * (self.newmaks_y - self.newmin_y) / (self.maks_y - self.minimal_y) + self.newmin_y
                feature[value] = newdata
        
        return feature