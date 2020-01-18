import time  # measure total run time of program
import pandas as pd
import requests
import re


def change_http_status_file(correction, input):
    no_of_checked_rows = 0

    for row_input in input.itertuples():
        if no_of_checked_rows % 100 == 0 and no_of_checked_rows != 0:
            print("Current process: ", no_of_checked_rows)
        for row_correction in correction.itertuples():
            # if no_of_checked_rows == 50:
            #     print("I'm out")
            #     return input
            if row_input.github_url == row_correction.github_url:
                input["github_url"].at[no_of_checked_rows] = row_correction.new_github_url
                input["github_user"].at[no_of_checked_rows] = row_correction.new_github_profile
                input["http_status"].at[no_of_checked_rows] = row_correction.new_status_code

        no_of_checked_rows += 1

    return input

# df.drop([0, 1])

def change_profile_data(correction, input):
    no_of_checked_rows = 0

    for row_input in input.itertuples():
        if no_of_checked_rows % 100 == 0 and no_of_checked_rows != 0:
            print("Current process: ", no_of_checked_rows)
        for row_correction in correction.itertuples():
            # if no_of_checked_rows == 100:
            #     print("I'm out")
            #     return input
            if row_input.github_user == row_correction.github_user:
                if row_correction.github_user != "problem":
                    print("Duplicate user found: ", row_input.github_user, "New name: ", row_correction.new_github_profile)
                    input["github_user"].at[no_of_checked_rows] = row_correction.new_github_profile
                    input["profile_data"].at[no_of_checked_rows] = None
                    input["login"].at[no_of_checked_rows] = None
                    input["type"].at[no_of_checked_rows] = None
                    input["company"].at[no_of_checked_rows] = None
                    input["blog"].at[no_of_checked_rows] = None
                    input["location"].at[no_of_checked_rows] = None
                    input["email"].at[no_of_checked_rows] = None
                    input["hireable"].at[no_of_checked_rows] = None
                    input["public_repos"].at[no_of_checked_rows] = None
                    input["public_gists"].at[no_of_checked_rows] = None
                    input["followers"].at[no_of_checked_rows] = None
                    input["following"].at[no_of_checked_rows] = None
                    input["created_at"].at[no_of_checked_rows] = None
                    input["updated_at"].at[no_of_checked_rows] = None

        no_of_checked_rows += 1
    return input

def write_to_csv_file(http_file, profile_data_file):
    print("in write")
    if http_file is not None:
        http_file.to_csv("new_http_status.csv", index = False)
    if profile_data_file is not None:
        profile_data_file.to_csv("new_profile_data_file.csv", index=False)

def main():
    print("Starting curl_requests_301_302.py:")
    start_time = time.time()

    correction_file = pd.read_csv("requests_301_302.csv", sep=",", keep_default_na=False,
                                  usecols=["github_url", "github_user", "http_status", "new_github_url",
                                           "new_github_profile", "new_status_code"])

    http_status = pd.read_csv("output_3_tmp.csv", sep=",", keep_default_na=False, index_col=0)
    profile_data = pd.read_csv("profile_data.csv", sep=",", keep_default_na=False, index_col=0)
    # new_df_http = change_http_status_file(correction_file, http_status)
    new_df_profile = change_profile_data(correction_file, profile_data)

    write_to_csv_file(None, new_df_profile)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
