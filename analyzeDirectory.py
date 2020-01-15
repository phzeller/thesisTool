import os  # file system operations
import numpy as np  # use numpy arrays for better performance

from main import profile
from notice import DMCA_notice
import conf
import sys #TODO FOR TESTING
import analyzeData

@profile
def processDirectory(directory):
    notice_int = 0
    for file in os.listdir(directory):
        return_value = checkPath(directory, file.lower())
        # If valid DMCA notice file found, create DMCA_notice object and proceed the analysis
        if return_value is not None:
            new_notice = DMCA_notice(return_value)  # create DMCA_notice object
            notice_int += 1
            # TODO TESTING
            testVar = 0 # 0 if no test, 1 if testing
            # normal behavior
            if testVar == 0:
                new_notice.mineData()  # mine all required data
                new_notice.create_list_for_mined_data()  # Merge all mined data into one list
                # write all values to csv file
                conf.write_to_csv_file(new_notice)
            # TESTING behavior
            else:
                # be aware, that filePath is lower case -> do not use upper case letters in if condition!
                if "coupons.md" in new_notice.filePath:
                    new_notice.mineData()  # mine all required data
                    new_notice.create_list_for_mined_data()  # Merge all mined data into one list
                    conf.write_to_csv_file(new_notice)
                    new_notice.testing()
                    conf.save_csv_file()
                    sys.exit(0)

@profile
def checkPath(dir, file):
    # First, check the content of the input directory (if content is file or directory)

    # TODO testing purposes
    # if conf.no_of_notices == 2000: return

    if (".git" in file) or ("data" in file) or (".DS_Store" in file):  # Ignore .git and data and .DS_Store folder
        return

    path = os.path.join(dir, file).lower()  # full path is required for isdir / isfile --> join content with previous path
    if os.path.isdir(path):  # Dig into each folder again
        processDirectory(path)
    elif os.path.isfile(path):
        # we only need .markdown or .md files for the analysis
        if any(requiredKeyword in path for requiredKeyword in (".markdown", ".md")):
            if not any(badKeyword in path for badKeyword in ("readme.md", "contributing.md")):
                return np.array([path, file])
            else:
                print("badKeyword found (program shall not process readme / contribution files): ", path)
        else:
            print("File does not contain .markdown or .md: " + path)
    else:
        print("No dir nor file: " + path)
    return
