import time  # measure total run time of program
import cProfile
import re
import pandas as pd
import requests

from io import StringIO


def check_http_status(input_data):
    no_of_checked_rows = 0
    no_of_added_http_status = 0

    for row in input_data.itertuples():
        if no_of_checked_rows % 100 == 0 and no_of_checked_rows != 0:
            print("Current process: ", no_of_checked_rows)

        # Each 100 added URLs: save backup to file
        if no_of_added_http_status % 100 == 0 and no_of_added_http_status != 0:
            print("Saving backup file")
            write_to_csv_file(input_data)
            print("Saved backup file")

        # TODO: TESTING
        # if no_of_added_http_status == 20:
        #     print("No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
        #           no_of_added_http_status)
        #     return input_data
        if row.no_of_github_URLs > 0 and len(row.http_status) == 0:
            try:
                http_status = requests.head(row.github_url)
            except Exception:
                print("Problem found with URL: ", row.github_url)
                input_data["http_status"].at[no_of_checked_rows] = "error"
            else:
                print(http_status.status_code)
                input_data["http_status"].at[no_of_checked_rows] = http_status.status_code
            finally:
                no_of_added_http_status += 1
        no_of_checked_rows += 1

    print("No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
          no_of_added_http_status)
    return input_data

def write_to_csv_file(input_data):
    input_data.to_csv("output_3_tmp.csv")


def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()

    csv_input = pd.read_csv("output_3_tmp.csv", sep=",", index_col=False, keep_default_na=False)
    csv_input.set_index("index", inplace=True)
    new_file = check_http_status(csv_input)
    write_to_csv_file(new_file)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
