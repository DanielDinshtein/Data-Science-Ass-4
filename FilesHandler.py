
import pandas as pd
import os


class FilesHandler:

    def __init__(self):
        self.folder_path = None



    def readFilesFromFolder(self, folderPath):
        """
        Called from the GUI after the user entered folder directory.
        This method is in charge to call the methods of files reading,
        and arrange the information before sending it back to the GUI.
        :param folderPath: The file folder directory with the need files
        :return: The file and the information of error if there was
        """
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
        """
        This method is in charge of reading the ' train.csv ' file,
        and check if it exist and with data.
        :return: The file if everything is valid, else the relevant error that occurred
        """
        try:
            trainSet = pd.read_csv(self.folder_path + "\\train.csv")
            return trainSet, None
        except IOError:
            return [], "The file ' train.csv ' doesn't exist in this folder"
        except pd.errors.EmptyDataError:
            return [], "The file ' train.csv ' is empty"



    def extractTestFile(self):
        """
        This method is in charge of reading the ' test.csv ' file,
        and check if it exist and with data.
        :return: The file if everything is valid, else the relevant error that occurred
        """
        try:
            testSet = pd.read_csv(self.folder_path + "\\test.csv")
            return testSet, None
        except IOError:
            return [], "The file ' test.csv ' doesn't exist in this folder"
        except pd.errors.EmptyDataError:
            return [], "The file ' test.csv ' is empty file"



    def extractStructureFile(self):
        """
        This method is in charge of reading the ' Structure.txt ' file,
        and check if it exist and with data.
        :return: The file if everything is valid, else the relevant error that occurred
        """
        try:
            file_size = os.stat(self.folder_path + "\\Structure.txt").st_size
            if file_size == 0:
                return [], "The file ' Structure.txt ' is empty file"

            with open(self.folder_path + "\\Structure.txt") as file:
                structure = file.readlines()
            file.close()

            return structure, None

        except IOError:
            return [], "The file ' Structure.txt ' doesn't exist in this folder"


