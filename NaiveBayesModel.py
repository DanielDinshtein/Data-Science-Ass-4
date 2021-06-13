
import pandas as pd


class NaiveBayesModel:

    def __init__(self):
        self.train_set = None
        self.features = None

        self.test_set = None
        self.prediction_result = {}
        self.folder_path = ""

        #  TODO: Remove After Every this working
        self.prediction_calculation = {}

        self.prior_probability = None
        self.likelihood = {}

        self.attributes_information = {}




    def buildModel(self, trainSet):
        """
        Called from the GUI after the user pressed the ' Build ' button.
        This method is in charge to call the methods of the model building ,
        and arrange the information before needed in time of classification.
        :param trainSet: The train data structure from building the model
        """
        self.train_set = trainSet
        self.features = trainSet.columns

        self.calculatePriorProbability()

        self.calculateLikelihood()



    def calculatePriorProbability(self):
        """
        This method is in charge of calculating the class values prior probability.
        It also saves the number of each value in each feature in the train set
        """
        for feature in self.features:

            if feature == "class" :
                self.prior_probability = self.train_set.groupby([feature]).size().div(len(self.train_set))

            self.attributes_information[feature] = self.train_set.groupby([feature]).size()



    def calculateLikelihood(self):
        """
        This method is in charge of calculating the likelihood of each feature
        with the m-estimate algorithm ( m = 2 )
        """
        for feature in self.features:

            if feature != "class" :
                Nc = self.train_set.groupby(["class", feature]).size()
                mp = 2 * ( 1 / len(self.attributes_information[feature]) )
                n = self.attributes_information["class"]

                self.likelihood[feature] = ( Nc + mp ) / ( n + 2 )



    def classifyTestSet(self, testSet, folderPath):
        """
        Called  from the GUI after the user pressed the ' Classify ' button.
        This method is in charge of the classification of all the test set,
        with the Naive Bayes - m-estimate Model
        :param testSet: The test set records needed to get classification
        :param folderPath: The Folder path where needed to write
               the ' output.txt ' file with the classification result
        """
        self.folder_path = folderPath

        labels = testSet.iloc[:, len(testSet.columns) - 1].values

        self.test_set = testSet.drop(["class"], axis=1)

        for index, row_to_classify in self.test_set.iterrows():

            self.prediction_result[ str( index + 1 ) ] = {}
            self.prediction_calculation[ str( index + 1 ) ] = {}

            for class_value in self.attributes_information["class"].index :

                self.prediction_result[ str( index + 1 ) ][ class_value ] = 1

                self.prediction_calculation[ str( index + 1 ) ][ class_value ] = { }

                for feature in row_to_classify.index :

                    feature_value = row_to_classify[ feature ]
                    feature_likelihood = self.likelihood[ feature ][ class_value ][ feature_value ]

                    self.prediction_result[str(index + 1)][ class_value ] *= feature_likelihood

                    self.prediction_calculation[ str(index + 1) ][ class_value ][ feature ] = feature_likelihood

                self.prediction_result[str(index + 1)][ class_value ] *= self.prior_probability[class_value]

        self.writePredictionResultToFile()



    def writePredictionResultToFile(self):
        """
        This method is in charge to right the prediction results to ' output.txt ' file
        """
        with open(self.folder_path + "\\output.txt", 'w') as file:

            for record_number, prediction_options in self.prediction_result.items() :

                max_val = 0
                prediction_class = ''
                for pred_option, option_value in prediction_options.items() :
                    if option_value > max_val :
                        max_val = option_value
                        prediction_class = pred_option

                output_line = record_number + " " + prediction_class

                if len(self.prediction_result) != int(record_number) :
                    output_line += "\n"

                file.write(output_line)
        file.close()

        #  TODO: Maybe try and except for file writing??

