
# HW4 : 312257116 _ 204415665 _ 206172686


from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox

from numpy.ma import column_stack

import FilesHandler


class GUI:

    def __init__(self, master):

        """--------------------------------- Init Attributes : ------------------------------------"""

        # Master Window
        self.master = master
        self.master.title("Naïve Bayes Classifier")
        self.master.geometry('520x600')

        self.number_of_bins = 0

        self.files_reader = FilesHandler.FilesHandler()



        """--------------------------------- Layout : ------------------------------------"""
        # File Path :

        #   Label
        self.file_path_label = Label(self.master, text="Directory Path : ")
        self.file_path_label.grid(row=0, column=0, sticky="W")

        #   Entry Or Label ??
        #  TODO: Entry Or Label?? :
        #   Does We Want Do Give The User The Option To Change The Path Manually
        # self.file_path_entry = Entry(self.master)
        # self.file_path_entry.grid(row=0, column=1)
        self.file_path_explorer_label = Label(self.master, text="Folder path", background="white", width="50")
        self.file_path_explorer_label.grid(row=0, column=1)

        #   Button
        self.browse_button = Button(self.master, text="Browse",  command=lambda: self.browseFileFolder())
        self.browse_button.grid(row=0, column=2)

        # Discretization Bins :

        #   Label :
        self.bins_label = Label(self.master, text="Discretization Bins : ")
        self.bins_label.grid(row=1, column=0, sticky="W")

        #   Entry
        checkValidBins = self.master.register(self.checkBinsNumber)
        self.bins_entry = Entry(self.master, validate="key", validatecommand=(checkValidBins, '%P'))
        self.bins_entry.grid(row=1, column=1, sticky="W" )



    def browseFileFolder(self):

        file_folder = filedialog.askdirectory(initialdir="/", title="Select a Folder")
        if file_folder is not None:

            files_handler_result = self.files_reader.readFilesFromFolder(file_folder)

            error_exists = False
            error_message = ""

            for file_name, result_about_file in files_handler_result.items():
                if result_about_file["Error"] is not None:
                    error_exists = True
                    error_message += result_about_file["Error"]
                    error_message += ".\n"

            if not error_exists :
                self.file_path_explorer_label.configure(text=file_folder)
            else:
                self.errorHandler(error_message)

        else :
            self.errorHandler("Please select valid file directory.")



    def errorHandler(self, errorMessage):

        messagebox.showerror("Naïve Bayes Classifier", errorMessage)



    def checkBinsNumber(self, binsText):

        if not binsText:
            self.number_of_bins = None
            return True

        try:
            self.number_of_bins = int(binsText)
            return True
        except ValueError:
            return False








root = Tk()
my_gui = GUI(root)
root.mainloop()
