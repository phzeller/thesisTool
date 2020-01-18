import time  # measure total run time of program
import pandas as pd
import requests
import re

def adjust_URL(input_data):
    no_of_checked_rows = 0
    no_of_added_updated_data = 0

    for row in input_data.itertuples():
        if no_of_checked_rows % 100 == 0 and no_of_checked_rows != 0:
            print("Current process: ", no_of_checked_rows)

        # Each 100 added URLs: save backup to file
        if no_of_added_updated_data % 100 == 0 and no_of_added_updated_data != 0:
            print("Saving backup file")
            write_to_csv_file(input_data)
            print("Saved backup file")

        # TODO: TESTING
        # if no_of_added_updated_data == 1:
        #     print("No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
        #           no_of_added_updated_data)
        #     return input_data
        if len(row.new_github_url) == 0:
            try:
                http_status = requests.head(row.github_url, allow_redirects=True)
            except Exception:
                print("Problem found with URL: ", row.github_url)
                input_data["new_status_code"].at[no_of_checked_rows] = "error"
            else:
                print(http_status.status_code)
                input_data["new_status_code"].at[no_of_checked_rows] = http_status.status_code
                input_data["new_github_url"].at[no_of_checked_rows] = http_status.url
                input_data["new_github_profile"].at[no_of_checked_rows] = add_profile_link(http_status.url)
            finally:
                no_of_added_updated_data += 1
        no_of_checked_rows += 1

    print("No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
          no_of_added_updated_data)
    return input_data

def add_profile_link(url):
    # three types of urls exist:
    # 1) https://github.com/"username"/"repository"(/..)* (also: https://gist.github.com/"username"(/..)*
    # 2) "username".github.io(/..)*
    # 3) githubusercontent.com/"username"(/..)*
    github_user_url = ""
    # print(url) # TODO
    regex_github_com = re.search(r"http[s]?://(?:www\.)?(?:gist\.)?github\.com/[\w]+[-]?[\w]*[\/]?", url, flags=re.IGNORECASE)
    regex_github_io = re.search(r"http[s]?://(?:www\.)?([\w]+[-]?[\w]*)\.github\.io[\/]?", url, flags=re.IGNORECASE)
    regex_githubusercontent_com = re.search(r"http[s]?://(?:www\.)?raw\.githubusercontent\.com/([\w]+[-]?[\w]*)[\/]?", url, flags=re.IGNORECASE)
    if regex_github_com is not None:
        # filter out anonymous profiles:
        regex_anonymous_url = re.search(r"(?:/anonymous/)", url, flags=re.IGNORECASE)
        if regex_anonymous_url is not None:
            return "anonymous"
        # transform https://gist.github.com/"username" into https://github.com/"username"
        github_user_url = regex_github_com.group(0).replace("//gist.", "//")
        return github_user_url
    elif regex_github_io is not None:
        return "https://github.com/"+regex_github_io.group(1)
    elif regex_githubusercontent_com is not None:
        return "https://github.com/"+regex_githubusercontent_com.group(1)

    # filter out private URLs
    elif "com/[private" in url:
        return "private"

    # filter out removed repositories
    elif "com/[repository" in url:
        return "repository removed"

    else:
        print("Problem with URL in add_profile_link method: ", url)
        return "problem"

def write_to_csv_file(input_data):
    input_data.to_csv("requests_301_302.csv")

def main():
    print("Starting curl_requests_301_302.py:")
    start_time = time.time()

    # csv_input = pd.read_csv("output_3_tmp.csv", sep=",", keep_default_na=False,
    #                         usecols=["github_url", "github_user", "http_status"], )
    #
    # # add columns
    # csv_input["new_github_url"] = ""
    # csv_input["new_github_profile"] = ""
    # csv_input["new_status_code"] = ""

    # # only use urls that return http status 301 or 302
    # new_df = csv_input.loc[(csv_input["http_status"] == "301") | (csv_input["http_status"] == "302")]

    csv_input = pd.read_csv("requests_301_302.csv", sep=",", keep_default_na=False, index_col=False, usecols=["github_url", "github_user", "http_status", "new_github_url", "new_github_profile", "new_status_code"])


    new_file = adjust_URL(csv_input)
    write_to_csv_file(new_file)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()