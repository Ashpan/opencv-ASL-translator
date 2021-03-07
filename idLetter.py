from collections import Counter


class idLetter():

    sampleCount = 0
    sampleData = {}
    sampleMax = 30
    sleepCount = 0
    sleepMax = 5

    def __init__(self, labelArray):
        for label in labelArray:
            self.sampleData[label] = 0
        print('Initialized sample\n')

    def addData(self, label, weight):
        if self.sampleCount >= self.sampleMax:
            k = Counter(self.sampleData)
            high = k.most_common(3)
            self.sampleData = dict.fromkeys(self.sampleData, 0)
            self.sampleCount = 0
            for i in range(len(high)):
                if(len(high[i][0]) <= 3):
                    high[i] = (high[i][0][2:], high[i][1])
                else:
                    high[i] = (high[i][0][3:], high[i][1])
            return (high)
        elif self.sleepCount < self.sleepMax:
            self.sleepCount += 1
        else:
            self.sampleCount += 1
            self.sampleData[label] += weight
            return None

    def reset(self):
        self.sleepCount = 0
        self.sampleCount = 0
        self.sampleData = dict.fromkeys(self.sampleData, 0)
