
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
        self.master.geometry('660x500')
        self.master.config(background="bisque")

        # Files Attributes
        self.folder_directory_path = ""
        self.number_of_bins = None
        self.train_set = None
        self.test_set = None
        self.structure = None

        # Flags For "Build" Button
        self.done_browse = False
        self.done_bin = False

        # Flag For "Classify" Button
        self.done_build = False

        # Flags And Error Message About Files
        self.error_build_files = False
        self.error_message_files = ""
        self.error_classify_files = False


        # Classes Objects
        self.files_handler = FilesHandler.FilesHandler()
        self.pre_processor = PreProcessing.PreProcessing()
        self.naive_bayes_model = NaiveBayesModel.NaiveBayesModel()



        """--------------------------------- Layout : ------------------------------------"""
        # File Path :

        #   Label
        self.file_path_label = Label(self.master, text="Directory Path : ")
        self.file_path_label.config(background="bisque", font="bold")
        self.file_path_label.grid(row=0, column=0, sticky="W", padx=5, pady=35)

        #   Label
        self.file_path_explorer_label = Label(self.master, text="Folder path", background="white", width="50", height="2", borderwidth=1, relief="solid")
        self.file_path_explorer_label.grid(row=0, column=1)

        #   Button
        self.browse_button = Button(self.master, text="Browse", width="10", height="2", relief="raised", command=lambda: self.browseFileFolder())
        self.browse_button.grid(row=0, column=2, padx=5)


        # Discretization Bins :

        #   Label
        self.bins_label = Label(self.master, text="Discretization Bins : ")
        self.bins_label.config(background="bisque", font="bold", height="2")
        self.bins_label.grid(row=1, column=0, sticky="W")

        #   Entry
        checkValidBins = self.master.register(self.checkBinsNumber)
        self.bins_entry = Entry(self.master, validate="key", validatecommand=(checkValidBins, '%P'))
        self.bins_entry.grid(row=1, column=1, sticky="W")


        # Build :

        #   Button
        self.build_button = Button(self.master, text="Build", command=lambda: self.startPreProcessing())
        self.build_button.config(state=DISABLED, relief=GROOVE, width="50", height="2")
        self.build_button.grid(row=4, column=1, pady=30)

        # Classify :

        #   Button
        self.classify_button = Button(self.master, text="Classify", command=lambda: self.startClassifier())
        self.classify_button.config(state=DISABLED, relief=GROOVE, width="50", height="2")
        self.classify_button.grid(row=6, column=1, pady=30)





    def browseFileFolder(self):
        """
        After the user pressing the ' Browse ' button, this method called.
        This method is in charge on the browse window for getting the file directory path.
        And after it got the user's input path, it's sends the path to the ' FileHandler '
        for read the needed files to the model.
        """
        need_to_rebuild = True

        if self.done_build :
            message = "Changing the directory path will restart the build process.\n\n"
            message += "Are you sure you want to change the directory path ?"
            need_to_rebuild = self.messageHandler("Want Rebuild?" , message)

        if not need_to_rebuild :
            return

        file_folder = filedialog.askdirectory(initialdir="/", title="Select a Folder")

        if file_folder is not None and file_folder != '' :

            # Change Directory Path
            self.folder_directory_path = file_folder
            self.file_path_explorer_label.configure(text=file_folder)

            # Read And Handel The Files
            files_handler_result = self.files_handler.readFilesFromFolder(file_folder)

            self.done_browse = True
            self.checkBuildButtonState()

            # Checks the input from the ' FilesHandler ' and update the attributes
            for file_name, result_about_file in files_handler_result.items():
                if result_about_file["Error"] is not None:
                    if file_name != "testSet" :
                        self.error_build_files = True
                        self.error_message_files += result_about_file["Error"]
                        self.error_message_files += ".\n\n"
                    else :
                        self.error_classify_files = True
                        self.error_message_files += result_about_file["Error"]
                        self.error_message_files += ".\n\n"


            # Save The Train And Test Files If No Errors
            if not self.error_build_files and not self.error_classify_files :
                self.train_set = files_handler_result["trainSet"]["File"]
                self.structure = files_handler_result["structure"]["File"]
                self.test_set = files_handler_result["testSet"]["File"]
            else :
                self.train_set = None
                self.structure = None
                self.test_set = None



    def startPreProcessing(self):
        """
        After the user pressing the ' Build ' button, this method called,
        and only if all of the user's input needed for the build are entered.
        This is in charge of all the " Build " stage -
            sends the files to preprocess
            send the data structure after preprocess to the model build
        :return:
        """
        if self.error_build_files or self.error_classify_files :
            self.messageHandler("Build Error", self.error_message_files)
            return

        # Pre Process Train Files
        pre_processing_result = self.pre_processor.preProcessBuildFiles(self.train_set, self.structure, self.number_of_bins)

        # Build The Model
        self.naive_bayes_model.buildModel(pre_processing_result)

        # Finish Building The Model
        self.messageHandler("Build Finished", "Building classifier using train-set is done!")



    def startClassifier(self):
        """
        After the user pressing the ' Classify ' button, this method called.
        This method is in charge of all the " Classification " stage -
            sends the test file to preprocess
            send the data structure after preprocess to the prediction model
        """
        # Pre Process Test File
        pre_processing_result = self.pre_processor.preProcessTestSet(self.test_set)

        # Make Classification On Test File
        self.naive_bayes_model.classifyTestSet(pre_processing_result, self.folder_directory_path)

        # Finish Classification - Exit The Program
        message = "All records are classified successfully ! \n\n"
        message += "The classification results are saved in the files folder in - 'output.txt'. "
        self.messageHandler("Finished Classify", message)



    def messageHandler(self, messageType, message):
        """
        This method called from the other methods in the class.
        It is in charge of handling the messages that need to be shown to the user.
        :param messageType: What case of message need to be shown
        :param message: The message that will be shown to the user
        :return: Only in case of ' ask question ' - return if user want to rebuild or not
        """
        if messageType == "Build Error" :
            messagebox.showerror(title="Naïve Bayes Classifier", message=message)
            self.rebootBuildAttributes()

        elif messageType == "Build Finished" :
            messagebox.showinfo(title="Naïve Bayes Classifier", message=message)
            self.rebootAfterBuildFinished()

        elif messageType == "Want Rebuild?" :
            result_from_ask_question = messagebox.askquestion(title="Naïve Bayes Classifier", message=message)
            if result_from_ask_question == 'yes' :
                self.rebootBuildAttributes()
                return True

            return False

        elif messageType == "Finished Classify" :
            messagebox.showinfo(title="Naïve Bayes Classifier", message=message)
            self.master.destroy()



    def checkBinsNumber(self, binsText):
        """
        This method is a validation function for ' Bins ' Entry object,
        It is in charge of handling the input in the Entry in the ' Bins ' object.
        :param binsText: The text from the user's input in the ' Bins ' entry
        :return: True - if its int ; False - else
        """
        if not binsText:
            self.number_of_bins = None
            self.done_bin = False
            self.checkBuildButtonState()
            return True

        try:
            self.number_of_bins = int(binsText)
            self.done_bin = True
            self.checkBuildButtonState()
            return True
        except ValueError:
            return False



    def checkBuildButtonState(self):
        """
        After every change in the ' Build buttons Flags' , this method called.
        This method is in charge on the change of the ' Build ' button state :
        The Button States :
        - NORMAL - When all needed user's inputs are given
        - DISABLED - When the user didn't finished to enter all the inputs needed
        """
        if self.done_browse and self.done_bin and self.build_button['state'] == DISABLED :
            self.build_button.config(state=NORMAL, relief=RAISED)

        elif self.build_button['state'] == NORMAL :
            if not self.done_browse or not self.done_bin :
                self.build_button.config(state=DISABLED, relief=GROOVE)



    def checkClassifyButtonState(self):
        """
        After every change in the ' Classify buttons Flags' , this method called.
        This method is in charge on the change of the ' Classify ' button state :
        The Button States :
        - NORMAL - The " Build " stage finished successfully
        - DISABLED - All time before " Build " executed successfully
        """
        if self.done_build and self.classify_button['state'] == DISABLED :
            self.classify_button.config(state=NORMAL, relief=RAISED)

        elif self.classify_button['state'] == NORMAL and not self.done_build :
            self.classify_button.config(state=DISABLED, relief=GROOVE)



    def rebootBuildAttributes(self):
        """
        This method is in charge to reboot all the attributes that
        indicate us about the ' Build ' stage.
        """
        # Browse Button
        self.done_browse = False
        self.checkBuildButtonState()

        # Directory Clear
        self.file_path_explorer_label.configure(text="Folder path")
        self.folder_directory_path = ""

        # Files Clear
        self.test_set = None
        self.train_set = None
        self.structure = None

        # Files Attributes clear
        self.error_build_files = False
        self.error_message_files = ""
        self.error_classify_files = False

        # Build Button
        self.done_build = False
        self.checkClassifyButtonState()



    def rebootAfterBuildFinished(self):
        """
        This method is in charge to reboot all the attributes that
        indicate us about the ' After Build ' stage.
        """
        self.done_build = True
        self.checkClassifyButtonState()

        self.done_browse = False
        self.checkBuildButtonState()






root = Tk()
my_gui = GUI(root)
root.mainloop()
