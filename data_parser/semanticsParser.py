import json

class SemanticsParser:
    semanticsObj = {}
    intensifier = {}
    positive = {}
    negative = {}

    def __init__(self):
        with open('semantics.json') as data_file:    
            self.semanticsObj = json.load(data_file)

        for row in self.semanticsObj['intensifier']:
            self.intensifier[row['phrase']] = row['multiplier']

        for row in self.semanticsObj['positive']:
            self.positive[row['phrase']] = row['value']

        for row in self.semanticsObj['negative']:
            self.negative[row['phrase']] = row['value']

    def getIntensifiers(self):
        return self.intensifier

    def getPositives(self):
        return self.positive

    def getNegatives(self):
        return self.negative
