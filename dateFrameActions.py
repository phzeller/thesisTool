import pandas as pd
import re  # use regex to make sure that certain format guidelines are followed
import time  # measure total run time of program
from ast import literal_eval  # datatype list get converted to string in .csv files


# Pro github URL soll nun eine Zeile erstellt werden
def one_row_each_URL(df):
    testInt = 0

    new_df = pd.DataFrame(columns=list(df))
    for row in df.itertuples():

        # TODO TEST delete testInt and if condition
        testInt += 1
        if testInt%100 == 0: print(testInt)
        # if testInt == 1000: return new_df

        if isinstance(row.github_url, str):  # NaN entries are treated as float, those should not be investigated
            github_url_converted = literal_eval(row.github_url)
            for url in github_url_converted:
                github_user_profile = add_profile_link(url)
                row_data = [row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice, row.copyright_holder,
                            url, 1, row.other_urls, row.no_of_other_URLs, github_user_profile]
                new_df.loc[len(new_df)] = row_data
        else:  # leave row untouched if no github URL available
            row_data = [row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice, row.copyright_holder,
                        row.github_url, row.no_of_github_URLs, row.other_urls, row.no_of_other_URLs, row.github_user]
            new_df.loc[len(new_df)] = row_data

    return new_df


def add_profile_link(url):
    # three types of urls exist:
    # 1) https://github.com/"username"/"repository"(/..)* (also: https://gist.github.com/"username"(/..)*
    # 2) "username".github.io(/..)*
    # 3) githubusercontent.com/"username"(/..)*
    github_user_url = ""
    # print(url) # TODO
    regex_github_com = re.search(r"http[s]?://(?:www\.)?(?:gist\.)?github\.com/[\w]+[-]?[\w]*[\/]?", url, flags=re.IGNORECASE)
    regex_github_io = ""
    regex_githubusercontent_com = ""

    if regex_github_com is not None:
        # filter out anonymous profiles:
        regex_anonymous_url = re.search(r"(?:/anonymous/)", url, flags=re.IGNORECASE)
        if regex_anonymous_url is not None:
            print("anonymous URL found: ", url)
            return "anonymous"

        # transform https://gist.github.com/"username" into https://github.com/"username"
        github_user_url = regex_github_com.group(0).replace("//gist.", "//")
        return github_user_url
    elif "github.io" in url:
        test = None
    elif "githubusercontent.com" in url:
        test = None
    else:
        print("Problem with URL in add_profile_link method: ", url)

    return github_user_url


def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()

    df_data = pd.read_csv("output.csv")
    new_df = one_row_each_URL(df_data)
    new_df.to_csv("output_2_test.csv")
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
