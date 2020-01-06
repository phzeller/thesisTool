import os  # file system operations
import numpy as np  # use numpy arrays for better performance

from notice import DMCA_notice
import conf
import sys #TODO FOR TESTING
import analyzeData


def processDirectory(directory):
    for file in os.listdir(directory):
        return_value = checkPath(directory, file)
        # If valid DMCA notice file found, create DMCA_notice object and proceed the analysis
        if isinstance(return_value, np.ndarray):
            new_notice = DMCA_notice(return_value)  # create DMCA_notice object
            new_notice.mineData()   # mine all required data
            new_notice.create_DF_for_mined_data() # Merge all mined data into one dataframe

            # write all values to dataframe
            conf.write_to_dataframe(new_notice)
            #TODO TESTING
            # if "Jiufu" in new_notice.filePath.lower():
            #     new_notice.testing()
            #     conf.write_to_csv()
            #     sys.exit(0)


def checkPath(dir, file):
    # First, check the content of the input directory (if content is file or directory)

    # TODO testing purposes
    # if conf.no_of_notices == 100: return

    if (".git" in file) or ("data" in file) or (".DS_Store" in file):  # Ignore .git and data and .DS_Store folder
        return 0

    path = os.path.join(dir, file)  # full path is required for isdir / isfile --> join content with previous path
    if os.path.isdir(path):  # Dig into each folder again
        processDirectory(path)
    elif os.path.isfile(path):
        # we only need .markdown or .md files for the analysis
        if any(requiredKeyword in path.lower() for requiredKeyword in (".markdown", ".md")):
            if not any(badKeyword in path.lower() for badKeyword in ("readme.md", "contributing.md")):
                conf.no_of_notices += 1
                return np.array([path, file])
            else:
                print("badKeyword found (program shall not process readme / contribution files): ", path)
        else:
            print("File does not contain .markdown or .md: " + path)
    else:
        print("No dir nor file: " + path)
    return 0
