
import pandas as pd


class NaiveBayesModel:

    def __init__(self):
        self.train_set = None
        self.features = None

        self.prior_probability = None
        self.likelihood = {}

        self.attributes_information = {}




    def buildModel(self, trainSet):
        self.train_set = trainSet
        self.features = trainSet.columns

        self.calculatePriorProbability()

        self.calculateLikelihood()




    def calculatePriorProbability(self):

        for feature in self.features:

            if feature == "class" :
                self.prior_probability = self.train_set.groupby([feature]).size()

            self.attributes_information[feature] = self.train_set.groupby([feature]).size()




    def calculateLikelihood(self):

        for feature in self.features:

            if feature != "class" :
                Nc = self.train_set.groupby(["class", feature]).size()
                mp = 2 * ( 1 / len(self.attributes_information[feature]) )
                n = self.attributes_information["class"]

                self.likelihood[feature] = ( Nc + mp ) / ( n + 2 )

                # y = self.likelihood[feature]['N']['Female']

