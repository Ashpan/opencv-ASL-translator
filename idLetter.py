class idLetter():

    sampleCount = 0
    sampleData = {}
    sampleMax = 10

    def __init__(self, labelArray):
        for label in labelArray:
            self.sampleData[label] = 0
        print('Initialized sample\n')

    def addData(self, label, weight):
        if self.sampleCount >= self.sampleMax:
            maxVal = 0
            maxLabel = ''
            for lab in self.sampleData:
                if self.sampleData[lab] >= maxVal:
                    maxVal = self.sampleData[lab]
                    maxLabel = lab
                self.sampleData[lab] = 0
            self.sampleCount = 0
            return maxLabel
        else:
            self.sampleCount += 1
            self.sampleData[label] += weight
            return None
