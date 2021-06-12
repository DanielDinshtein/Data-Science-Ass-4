
# HW4 : 312257116 _ 204415665 _ 206172686


from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox, DISABLED, NORMAL, GROOVE, RAISED

import FilesHandler
import PreProcessing
import NaiveBayesModel


class GUI:

    def __init__(self, master):

        """--------------------------------- Init Attributes : ------------------------------------"""

        # Master Window
        self.master = master
        self.master.title("Naïve Bayes Classifier")
        self.master.geometry('600x600')
        self.master.config(background="bisque")

        # Files Attributes
        self.folder_directory_path = ""
        self.number_of_bins = None
        self.train_set = None
        self.test_set = None
        self.structure = None

        # Flags For "Build" Button
        self.is_done_browse = False
        self.is_done_bin = False

        # Flag For "Classify" Button
        self.done_build = False

        # Flags And Error Message About Files
        self.error_build_files = False
        self.error_message_build_files = ""
        self.error_classify_files = False
        self.error_message_classify_files = ""

        # Classes Objects
        self.files_handler = FilesHandler.FilesHandler()
        self.pre_processor = PreProcessing.PreProcessing()
        self.naive_bayes_model = NaiveBayesModel.NaiveBayesModel()



        """--------------------------------- Layout : ------------------------------------"""
        # File Path :

        #   Label
        self.file_path_label = Label(self.master, text="Directory Path : ")
        self.file_path_label.config(background="bisque", font="bold")
        self.file_path_label.grid(row=0, column=0, sticky="W")

        #   Entry Or Label ??
        #   TODO: Does We Want Do Give The User The Option To Change The Path Manually
        # self.file_path_entry = Entry(self.master)
        # self.file_path_entry.grid(row=0, column=1)
        self.file_path_explorer_label = Label(self.master, text="Folder path", background="white", width="50")
        self.file_path_explorer_label.grid(row=0, column=1)

        #   Button
        self.browse_button = Button(self.master, text="Browse",  command=lambda: self.browseFileFolder())
        self.browse_button.grid(row=0, column=2)


        # Discretization Bins :

        #   Label
        self.bins_label = Label(self.master, text="Discretization Bins : ")
        self.bins_label.config(background="bisque", font="bold")
        self.bins_label.grid(row=1, column=0, sticky="W")

        #   Entry
        checkValidBins = self.master.register(self.checkBinsNumber)
        self.bins_entry = Entry(self.master, validate="key", validatecommand=(checkValidBins, '%P'))
        self.bins_entry.grid(row=1, column=1, sticky="W" )


        # Build :

        #   Button
        self.build_button = Button(self.master, text="Build", command=lambda: self.startPreProcessing())
        self.build_button.config(state=DISABLED, relief=GROOVE)
        self.build_button.grid(row=2, column=1)

        # Classify :

        #   Button
        self.classify_button = Button(self.master, text="Classify", command=lambda: self.startClassifier())
        self.classify_button.config(state=DISABLED, relief=GROOVE)
        self.classify_button.grid(row=3, column=1)





    def browseFileFolder(self):

        file_folder = filedialog.askdirectory(initialdir="/", title="Select a Folder")
        if file_folder is not None and file_folder != '':

            # Change Directory Path
            self.folder_directory_path = file_folder
            self.file_path_explorer_label.configure(text=file_folder)

            # Read And Handel The Files
            files_handler_result = self.files_handler.readFilesFromFolder(file_folder)

            self.is_done_browse = True
            self.checkBuildButtonState()

            self.error_build_files = False
            self.error_classify_files = False

            for file_name, result_about_file in files_handler_result.items():
                if result_about_file["Error"] is not None:
                    if file_name != "testSet" :
                        self.error_build_files = True
                        self.error_message_build_files += result_about_file["Error"]
                        self.error_message_build_files += ".\n"
                    else :
                        self.error_classify_files = True
                        self.error_message_classify_files += result_about_file["Error"]

            # Save The Train Files If No Errors
            if not self.error_build_files :
                self.train_set = files_handler_result["trainSet"]["File"]
                self.structure = files_handler_result["structure"]["File"]
            else :
                self.train_set = None
                self.structure = None

            # Save The Test File If No Errors
            if not self.error_classify_files :
                self.test_set = files_handler_result["testSet"]["File"]
            else :
                self.test_set = None


        else :
            self.is_done_browse = False
            self.checkBuildButtonState()
            # self.errorHandler("Please select valid file directory.")



    def startPreProcessing(self):

        if self.error_build_files:
            self.messageHandler("Build Error", self.error_message_build_files)
            return

        pre_processing_result = self.pre_processor.preProcessBuildFiles(self.train_set, self.structure, self.number_of_bins)

        #  TODO: Clear train_set maybe?
        # What To Do After Building ?

        self.naive_bayes_model.buildModel(pre_processing_result)

        self.messageHandler("Build Finished", "Building classifier using train-set is done!")




    def startClassifier(self):
        pass



    def messageHandler(self, messageType, message):

        if messageType == "Build Error" :
            messagebox.showerror(title="Naïve Bayes Classifier", message=message)
            self.rebootAfterBuildError()
        elif messageType == "Build Finished" :
            messagebox.showinfo(title="Naïve Bayes Classifier", message=message)
            self.rebootAfterBuildFinished()



    def checkBinsNumber(self, binsText):
        #  TODO: Maybe Bins need to be smaller then len(test)??
        if not binsText:
            self.number_of_bins = None
            self.is_done_bin = False
            self.checkBuildButtonState()
            return True

        try:
            self.number_of_bins = int(binsText)
            self.is_done_bin = True
            self.checkBuildButtonState()
            return True
        except ValueError:
            return False


    def checkBuildButtonState(self):
        if self.is_done_browse and self.is_done_bin and self.build_button['state'] == DISABLED :
            self.build_button.config(state=NORMAL, relief=RAISED)

        elif self.build_button['state'] == NORMAL :
            if not self.is_done_browse or not self.is_done_bin :
                self.build_button.config(state=DISABLED, relief=GROOVE)

    def checkClassifyButtonState(self):
        if self.done_build and self.classify_button['state'] == DISABLED :
            self.classify_button.config(state=NORMAL, relief=RAISED)

        elif self.classify_button['state'] == NORMAL and not self.done_build :
            self.classify_button.config(state=DISABLED, relief=GROOVE)




    def rebootAfterBuildError(self):

        self.is_done_browse = False
        self.checkBuildButtonState()
        self.file_path_explorer_label.configure(text="Folder path")

        self.test_set = None
        self.train_set = None
        self.structure = None

        self.error_build_files = False
        self.error_message_build_files = ""
        self.error_classify_files = False
        self.error_message_classify_files = ""

    def rebootAfterBuildFinished(self):

        self.done_build = True
        self.checkClassifyButtonState()

        #  TODO : It's Ok To Disable Build ??
        self.is_done_browse = False
        self.checkBuildButtonState()










root = Tk()
my_gui = GUI(root)
root.mainloop()
