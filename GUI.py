
# HW4 : 312257116 _ 204415665 _ 206172686


from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox, DISABLED, NORMAL, GROOVE, RAISED

from numpy.ma import column_stack

import FilesHandler
import PreProcessing


class GUI:

    def __init__(self, master):

        """--------------------------------- Init Attributes : ------------------------------------"""

        # Master Window
        self.master = master
        self.master.title("Naïve Bayes Classifier")
        self.master.geometry('600x600')
        self.master.config(background="bisque")

        self.number_of_bins = None
        self.train_set = None
        self.test_set = None
        self.structure = None

        self.is_done_browse = False
        self.is_done_bin = False

        self.error_from_files = False
        self.error_message_from_files = ""

        self.files_reader = FilesHandler.FilesHandler()
        self.preProcessor = PreProcessing.PreProcessing()



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





    def browseFileFolder(self):

        file_folder = filedialog.askdirectory(initialdir="/", title="Select a Folder")
        if file_folder is not None and file_folder != '':

            self.file_path_explorer_label.configure(text=file_folder)

            files_handler_result = self.files_reader.readFilesFromFolder(file_folder)

            self.is_done_browse = True
            self.checkBuildButtonState()
            self.error_from_files = False

            for file_name, result_about_file in files_handler_result.items():
                if result_about_file["Error"] is not None:
                    self.error_from_files = True
                    self.error_message_from_files += result_about_file["Error"]
                    self.error_message_from_files += ".\n"

            if not self.error_from_files :
                self.train_set = files_handler_result["trainSet"]["File"]
                self.test_set = files_handler_result["testSet"]["File"]
                self.structure = files_handler_result["structure"]["File"]

        else :
            self.is_done_browse = False
            # self.errorHandler("Please select valid file directory.")



    def errorHandler(self, errorMessage):

        messagebox.showerror("Naïve Bayes Classifier", errorMessage)



    def checkBinsNumber(self, binsText):
        #  TODO: Maybe Bins need to be smaller then values??
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


    def startPreProcessing(self):

        if self.error_from_files:
            self.is_done_browse = False
            self.checkBuildButtonState()
            self.file_path_explorer_label.configure(text="Folder path")
            self.errorHandler(self.error_message_from_files)
            self.error_message_from_files = ""
            return



    def checkBuildButtonState(self):
        if self.is_done_browse and self.is_done_bin and self.build_button['state'] == DISABLED :
            self.build_button.config(state=NORMAL, relief=RAISED)

        elif self.build_button['state'] == NORMAL :
            if not self.is_done_browse or not self.is_done_bin :
                self.build_button.config(state=DISABLED, relief=GROOVE)








root = Tk()
my_gui = GUI(root)
root.mainloop()
