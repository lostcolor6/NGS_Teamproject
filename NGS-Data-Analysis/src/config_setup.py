import os
import shutil
def reset_config():
    """
    Resets the config file
    """
    with open("../.config/ngs_analysis_config.txt", 'w') as file:
        file.write("SeqPurge_Path=\n>\nBWA_Path=\n>\nsamblaster_Path=\n>\nsamtools_Path=\n>\nABRA2_Path=\n>\nfreebayes_Path=\n>\nvcfallelicprimitives_Path=\n>\nVcfBreakMulti_Path=\n>\nVcfLeftNormalize_Path=\n>")


def are_paths_valid(path_dict):
    """
    Checks if the paths in the config file are valid file paths
    :param path_dict: dictionary with the paths to the programs
    :return: boolean, True if all paths are valid, False if not
    """
    isValid = True
    for key in path_dict:
        if path_dict[key] == "":
            isValid=False
            print(f"{key} in config-file is empty. Please add the filepath to the programm to the config file.\n")
        elif not os.path.isfile(path_dict[key]):
            if shutil.which(path_dict[key]) is None:
                print(f"{key} is invalid. Please input correct filepath to programm in the config file or make sure the Programm is in $PATH. \nPlease edit the file in /.config and correct the path.\n")
                isValid = False
    return isValid


def get_Paths():
    """
    Reads the paths to the analysis programm from the config file and returns them as a dictionary
    :return: dict containg file paths
    """
    config_file = open("../.config/ngs_analysis_config.txt")
    path_dict = {}
    for line in config_file:
        if line != ">\n":
            programm_name, seperator, path = line.partition("=")
            path_dict[programm_name] = path[:-1]
    return path_dict