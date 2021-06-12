

import pandas as pd
import statistics as stats


class PreProcessing:

    def __init__(self):
        self.structure_file = None
        self.train_set = None
        self.test_set = None
        self.bins_number = 0


    def preProcessBuildFiles(self, trainSet, structureFile, binsNumber):
        self.structure_file = structureFile
        self.train_set = trainSet
        self.bins_number = binsNumber

        self.fillMissingValues()

        copy_train_set = self.train_set

        for idx, feature in enumerate(copy_train_set.columns):

            # No Need To Do Discretization On 'class'
            if "class" in self.structure_file[idx] or len(self.structure_file) == idx + 1 :
                #  TODO: What if 'class' is numeric??
                break

            # Numeric Attribute
            if "NUMERIC" in self.structure_file[idx] :
                self.train_set[feature] = self.equalWidthDiscretization(feature, "train")

        return self.train_set


    def preProcessTestSet(self, testSet):
        self.test_set = testSet

        copy_test_set = self.test_set

        for idx, feature in enumerate(copy_test_set.columns):

            # No Need To Do Discretization On 'class'
            if "class" in self.structure_file[idx] or len(self.structure_file) == idx + 1 :
                break

            # Numeric Attribute
            if "NUMERIC" in self.structure_file[idx] :
                self.test_set[feature] = self.equalWidthDiscretization(feature, "test")

        return self.test_set



    def fillMissingValues(self):

        # Get All Features With Nulls
        featuresWithNulls = self.train_set.apply(lambda x: sum(x.isnull()), axis=0)

        for idx, feature in enumerate(featuresWithNulls.index):

            # No Need To Fill 'class' Attribute
            if "class" in self.structure_file[idx] or len(self.structure_file) == idx + 1 :
                break

            # Check If There Null Values
            if featuresWithNulls[feature] != 0:
                # Categorical Attribute
                if "NUMERIC" not in self.structure_file[idx] :
                    self.train_set[feature].fillna(stats.mode(self.train_set[feature]), inplace=True)

                # Numeric Attribute
                elif "NUMERIC" in self.structure_file[idx] :
                    #  TODO: check if need to mean with group by on class
                    self.train_set[feature].fillna(self.train_set[feature].mean(), inplace=True)



    def equalWidthDiscretization(self, feature, trainOrTest):

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


