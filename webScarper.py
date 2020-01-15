import time  # measure total run time of program
import cProfile
import re
import pandas as pd
import requests

from csv import writer
from io import StringIO

# TODO get new github URL location if 301 http code!
def check_http_status(df):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    header = list(df)
    csv_writer.writerow(header)

    testInt = 0

    for row in df.itertuples():
        # Show progress
        if testInt%100 == 0:
            print(testInt)
        # if testInt == 5:
        #     return new_df_csv
        testInt += 1
        if row.no_of_github_URLs > 0 and len(row.http_status) == 0:
            print("URL:", row.github_url)
            http_status = requests.head(row.github_url)
            print(http_status)
            row_data = [row.index, row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice,
                        row.description, row.github_url, row.no_of_github_URLs, row.other_urls, row.no_of_other_URLs,
                        row.github_user, http_status]
            csv_writer.writerow(row_data)

    return new_df_csv




def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()
    df_data = pd.read_csv("output_2_final.csv", keep_default_na=False)

    with open("output_3_old_tmp.csv", mode="w") as output_file:
        new_df = check_http_status(df_data)
        output_file.write(new_df.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
