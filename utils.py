# Contains functions useful in more than one file
import os

def gather_names(dirpath):
    """ Gets all names of the molecules from the input molecule folder """
    
    all_names = list()
    for file in os.listdir(dirpath):
        if file.endswith(".xyz"):
            all_names.append(file[:-4])

    return all_names