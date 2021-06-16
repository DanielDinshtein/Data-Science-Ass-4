

import pandas as pd
import statistics as stats


class PreProcessing:

    def __init__(self):
        self.structure_file = None
        self.train_set = None
        self.test_set = None
        self.bins_number = 0



    def preProcessFiles(self, trainSet, structureFile, testSet, binsNumber):
        """
        Called from the GUI after the user pressed the ' Build ' button.
        This method is in charge to call the methods of the data structure preparations,
        and arrange the information before sending it back to the GUI.
        :param testSet: The test set file for classify the model
        :param trainSet: The train set file for building the model
        :param structureFile: The structure file with the information about the data attributes
        :param binsNumber: The number of bins for the Discretization
        :return: The train data structure after preprocessing
        """
        self.structure_file = structureFile
        self.train_set = trainSet
        self.test_set = testSet
        self.bins_number = binsNumber


        invalidFiles, message = self.checkIfAllFeaturesExists()

        if invalidFiles :
            return invalidFiles, message, None, None


        invalidFiles, message = self.fillMissingValues()

        if invalidFiles:
            return invalidFiles, message, None, None

        try :
            for idx, feature_structure in enumerate(self.structure_file):

                feature = feature_structure.split(' ')[1]

                # No Need To Do Discretization On 'class'
                if "class" in self.structure_file[idx] or len(self.structure_file) == idx + 1 :
                    break

                # Numeric Attribute
                if "NUMERIC" in self.structure_file[idx] :
                    self.train_set[feature] = self.equalWidthDiscretization(feature, "train")
                    self.test_set[feature] = self.equalWidthDiscretization(feature, "test")
        except :
            invalidFiles = True
            message += "Error in the Discretization features.\n"


        if invalidFiles :
            return invalidFiles, message, None, None

        return invalidFiles, message, self.train_set, self.test_set



    def checkIfAllFeaturesExists(self):

        invalidFiles = False
        message = ""

        try :
            for feature_structure in self.structure_file:
                feature = feature_structure.split(' ')[1]
                if feature not in self.train_set.columns:
                    message = message + "The feature : " + feature + " not found in the train set.\n"
                    invalidFiles = True
                if feature not in self.test_set.columns:
                    message = message + "The feature : " + feature + " not found in the test set.\n"
                    invalidFiles = True

        except :
            invalidFiles = True
            message += "Error in the features structures.\n"

        return invalidFiles, message


    def fillMissingValues(self):
        """
        This method is in charge of filling the missing values of the data attributes
        - Numeric - With the mean of all other records of this feature with the same same class
        - Categorical - With the most common value of all other values on this feature
        """
        invalidFiles = False
        message = ""

        try :
            connectedDataFrames = pd.concat([ self.train_set, self.test_set ])

            # Get All Features With Nulls
            trainSet_featuresWithNulls = self.train_set.apply(lambda x: sum(x.isnull()), axis=0)
            testSet_featuresWithNulls = self.test_set.apply(lambda x: sum(x.isnull()), axis=0)

            for idx, feature_structure in enumerate(self.structure_file):

                feature = feature_structure.split(' ')[1]

                # No Need To Fill 'class' Attribute
                if "class" in self.structure_file[idx] or len(self.structure_file) == idx + 1 :
                    break

                # Check If There Null Values - train
                if trainSet_featuresWithNulls[feature] != 0:
                    # Categorical Attribute
                    if "NUMERIC" not in self.structure_file[idx] :
                        self.train_set[feature].fillna(stats.mode(connectedDataFrames[feature]), inplace=True)

                    # Numeric Attribute
                    elif "NUMERIC" in self.structure_file[idx] :
                        self.train_set[feature] = self.train_set[feature].fillna(connectedDataFrames.groupby( "class" )[feature].transform("mean")[  : len(self.train_set) ])

                # Check If There Null Values - test
                if testSet_featuresWithNulls[feature] != 0:
                    # Categorical Attribute
                    if "NUMERIC" not in self.structure_file[idx] :
                        self.test_set[feature].fillna(stats.mode(connectedDataFrames[feature]), inplace=True)

                    # Numeric Attribute
                    elif "NUMERIC" in self.structure_file[idx] :
                        self.test_set[feature] = self.test_set[feature].fillna(connectedDataFrames.groupby( "class" )[feature].transform("mean")[ len(self.train_set) : ])
        except :
            invalidFiles = True
            message += "Error in the filling NA values.\n"

        return invalidFiles, message



    def equalWidthDiscretization(self, feature, trainOrTest):
        """
        This method is in charge of making discretization on the numeric attributes
        :param feature: The feature name need to get discretization
        :param trainOrTest: From which data set - train ot test
        :return: The feature values after the discretization
        """
        bins = []
        group_names = []

        if trainOrTest == "train" :
            min_value = self.train_set[feature].min()
            max_value = self.train_set[feature].max()
        else:
            # == test
            min_value = self.test_set[feature].min()
            max_value = self.test_set[feature].max()

        interval_width = ( max_value - min_value ) / self.bins_number

        for i in range(self.bins_number - 1) :
            bins.append( min_value + interval_width*( i + 1) )
            group_names.append( str(i) )

        group_names.append( str( self.bins_number - 1 ) )

        if trainOrTest == "train" :
            feature_binned = self.binning( self.train_set[feature], bins, group_names )
        else:
            # == test
            feature_binned = self.binning( self.test_set[feature], bins, group_names )


        return feature_binned



    def binning(self, col, cut_points, labels=None):
        # Define min and max values:
        minval = col.min()
        maxval = col.max()
        # create list by adding min and max to cut_points
        break_points = [minval] + cut_points + [maxval]
        # if no labels provided, use default labels 0 ... (n-1)
        if not labels:
            labels = range(len(cut_points) + 1)
        # Binning using cut function of pandas
        colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
        return colBin


