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
    new_header = list(input)
    # new_header.insert(0, "index")
    csv_writer.writerow(new_header)

    # for row in df.itertuples():
    #     if row.no_of_github_URLs > 0:
    #         github_url_converted = literal_eval(row.github_url)
    #         for url in github_url_converted:
    #             github_user_profile = add_profile_link(url)
    #             row_data = [indexInt, row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice, row.description,
    #                         url, 1, row.other_urls, row.no_of_other_URLs, github_user_profile, None]
    #             csv_writer.writerow(row_data)
    #             indexInt += 1
    #             # new_df.loc[len(new_df)] = row_data
    #     else:  # leave row untouched if no github URL available
    #         row_data = [indexInt, row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice, row.description,
    #                     row.github_url, row.no_of_github_URLs, row.other_urls, row.no_of_other_URLs, row.github_user, None]
    #         csv_writer.writerow(row_data)
    #         indexInt += 1
    # # new_df_csv.seek(0)
    # return new_df_csv

def main():
    print("Starting clean_org_and_NAs.py:")
    start_time = time.time()

    csv_input = pd.read_csv("activity_data_v2.csv", sep=",", keep_default_na=False, index_col=0,
                            usecols=lambda col: col not in ["profile_data"])


    with open("profile_data_unique_no_dup_no_org_no_NA.csv", mode="w") as output_file:
        new_df = create_activity_table(csv_input)
        # output_file.write(new_df.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()