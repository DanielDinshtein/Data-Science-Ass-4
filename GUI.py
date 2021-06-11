
# HW4 : 312257116 _ 204415665 _ 206172686


from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog

import FilesHandler


class GUI:

    def __init__(self, master):

        """--------------------------------- Init Attributes : ------------------------------------"""

        # Master Window
        self.master = master
        master.title("Naïve Bayes Classifier")

        self.files_reader = FilesHandler.FilesHandler()



        """--------------------------------- Layout : ------------------------------------"""
        # File Path :

        #   Babel
        self.file_path_label = Label(master, text="Directory Path")
        self.file_path_label.grid(row=0, column=0)

        #   Entry
        self.file_path_entry = Entry(master)
        self.file_path_entry.grid(row=0, column=1)

        # # Button
        self.browse_button = Button(master, text="Browse",  command=lambda: self.browseFileFolder())
        self.browse_button.grid(row=0, column=2)




    def browseFileFolder(self):
        file_folder = filedialog.askdirectory(initialdir="/", title="Select a Folder")
        if file_folder is not None:
            files_reader_result = self.files_reader.readFilesFromFolder(file_folder)







root = Tk()
my_gui = GUI(root)
root.mainloop()
