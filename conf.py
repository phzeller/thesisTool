import pandas as pd  # use pandas data frame as efficient data table
import numpy as np  # use numpy arrays for better performance

#   Configure the DMCA dataset directory below
######################################################
main_directory = "/Users/philippzeller/GitHub/dmca"  #
######################################################

# Do not touch those variables
no_of_notices = 0
output_df = None
output_fileName = "output.csv"


def createDataframe():
    global output_df
    # Define header of output file
    # TODO: include entire content in order to check duplicates
    header_data = np.array(
        ["year", "month", "day", "header", "notice", "copyright_holder", "github_url", "copyright_url", "github_user"])
    output_df = pd.DataFrame(columns=header_data)


def write_to_dataframe(noticeObj):
    output_df.loc[len(output_df)] = noticeObj.mined_list


def write_to_csv():
    # save dataframe to .csv ; index = False, sonst wird immer wieder ein neuer Index im output generiert
    output_df.to_csv(output_fileName)
