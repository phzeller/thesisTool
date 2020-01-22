import pandas as pd
import re  # use regex to make sure that certain format guidelines are followed
import time  # measure total run time of program
from ast import literal_eval  # datatype list get converted to string in .csv files

from csv import writer
from io import StringIO

def eliminate_ORGs_and_NAs(input_df):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    new_header = list(input_df)
    new_header.insert(0, None)
    csv_writer.writerow(new_header)

    index_counter = 0

    for row in input_df.itertuples():
        if row.type.lower() is not None and row.type.lower() == "user":
            index_counter += 1
            row_data = [index_counter, row.github_user, row.login, row.type, row.company, row.blog, row.location,
                        row.email, row.hireable, row.public_repos, row.public_gists, row.followers, row.following,
                        row.created_at, row.updated_at]

            csv_writer.writerow(row_data)

    return new_df_csv


def main():
    print("Starting clean_org_and_NAs.py:")
    start_time = time.time()

    csv_input = pd.read_csv("profile_data_unique_no_dup.csv", sep=",", keep_default_na=False, index_col=0,
                            usecols=lambda col: col not in ["profile_data"])


    with open("profile_data_unique_no_dup_no_org_no_NA.csv", mode="w") as output_file:
        new_df = eliminate_ORGs_and_NAs(csv_input)
        output_file.write(new_df.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
