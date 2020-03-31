import pandas as pd
import re  # use regex to make sure that certain format guidelines are followed
import time  # measure total run time of program
from ast import literal_eval  # datatype list get converted to string in .csv files

from csv import writer
from io import StringIO

def create_activity_table(input):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    new_header = [None, "login", "created_at", "date", "no_of_events"]
    csv_writer.writerow(new_header)

    for row in input.itertuples():
        index = getattr(row, "Index")
        # TODO: testing
        if index == 200:
            break

        print(len(row.activity_data))
        # Filter out repositories and NA entries

    return new_df_csv

def main():
    print("Starting select_activity.py:")
    start_time = time.time()

    csv_input = pd.read_csv("activity_data_v2.csv", sep=",", keep_default_na=False, index_col=0)

    with open("profile_data_unique_no_dup_no_org_no_NA.csv", mode="w") as output_file:
        new_df = create_activity_table(csv_input)
        # output_file.write(new_df.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()