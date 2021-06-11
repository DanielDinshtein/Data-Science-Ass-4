
import pandas as pd
import os


class FilesHandler:

    def __init__(self):
        self.folder_path = None



    def readFilesFromFolder(self, folderPath):

        self.folder_path = folderPath


        trainSet, TrainError = self.extractTrainFile()
        testSet, TestError = self.extractTestFile()
        structure, StructureError = self.extractStructureFile()

        resultFromReading = {
            "trainSet": {"File": trainSet, "Error": TrainError},
            "testSet": {"File": testSet, "Error": TestError},
            "structure": {"File": structure, "Error": StructureError}
        }

        return resultFromReading



    def extractTrainFile(self):

        try:
            trainSet = pd.read_csv(self.folder_path + "\\train.csv")
            return trainSet, None
        except IOError:
            return [], "train.csv doesn't exist in this folder"
        except pd.errors.EmptyDataError:
            return [], "train.csv is empty file"


    def extractTestFile(self):

        try:
            testSet = pd.read_csv(self.folder_path + "\\test.csv")
            return testSet, None
        except IOError:
            return [], "test.csv doesn't exist in this folder"
        except pd.errors.EmptyDataError:
            return [], "test.csv is empty file"


    def extractStructureFile(self):

        try:
            file_size = os.stat(self.folder_path + "\\Structure.txt").st_size
            if file_size == 0:
                return [], "Structure.txt is empty file"

            with open(self.folder_path + "\\Structure.txt") as file:
                structure = file.readlines()
            file.close()

            return structure, None

        except IOError:
            return [], "Structure.txt doesn't exist in this folder"


