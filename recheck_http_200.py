import time  # measure total run time of program
import pandas as pd
import requests
from bs4 import BeautifulSoup

import cProfile, pstats, io
from pstats import SortKey
import io

# line profiling
import line_profiler
import atexit
profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)

@profile
def recheck_URL(input_data):
    no_of_added_updated_data = 0
    for row in input_data.itertuples():
        index = getattr(row, "Index")

        if index % 100 == 0 and index != 0:
            print("Current process: ", index)

        # Each 100 added URLs: save backup to file
        if index % 5000 == 0 and index != 0:
            print("Saving backup file")
            write_to_csv_file(input_data)
            print("Saved backup file")

        # TODO: TESTING
        # if no_of_added_updated_data == 1:
        #     print("No. of checked rows in total: ", index, "while added this amout of rows: ",
        #           no_of_added_updated_data)
        #     return input_data
        if row.http_status == "200":
            page = requests.get(row.github_url, allow_redirects=True)
            soup = BeautifulSoup(page.content, 'lxml')
            content = soup.select(".blankslate > p:nth-child(3)")
            for section in content:
                if "access to this repository has been disabled by github staff" in section.text.lower():
                    print("Found removed URL: ", row.github_url)
                    print("in Notice ID: ", row.notice_id)
                    input_data["http_status"].at[index] = "451.1"
                    no_of_added_updated_data += 1

            # try:
            #     page = requests.get(row.github_url, allow_redirects=True)
            #     soup = BeautifulSoup(page.content, 'lxml')
            # except Exception:
            #     print("Problem found with URL: ", row.github_url)
            #     input_data["new_status_code"].at[index] = "error"
            # else:
            #     content = soup.select(".blankslate > p:nth-child(3)")
            #     for section in content:
            #         if "access to this repository has been disabled by github staff" in section.text.lower():
            #             print("Found removed URL: ", row.github_url)
            #             input_data["http_status"].at[index] = "451-1"
            #             no_of_added_updated_data += 1

    print("No. of checked rows in total: ", index, "while added this amout of rows: ",
          no_of_added_updated_data)
    return input_data


def write_to_csv_file(input_data):
    input_data.to_csv("GitHub_URLs_HTTP_status_v3.csv")


def main():
    print("recheck_http_200.py:")
    start_time = time.time()

    csv_input = pd.read_csv("/Users/philippzeller/Desktop/05_GitHub_URLs_HTTP_status_v2.csv" , sep=",", keep_default_na=False)

    new_file = recheck_URL(csv_input)
    write_to_csv_file(new_file)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()