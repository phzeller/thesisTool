import pandas as pd
import re  # use regex to make sure that certain format guidelines are followed
import time  # measure total run time of program
from ast import literal_eval  # datatype list get converted to string in .csv files

from csv import writer
from io import StringIO

# cProfiler
import cProfile, pstats, io
from pstats import SortKey
import io

# line profiler
# import line_profiler
# import atexit
# profile = line_profiler.LineProfiler()
# atexit.register(profile.print_stats)

# Credits to Sebastiaan Mathôt (https://www.youtube.com/watch?v=8qEnExGLZfY&t=915s) for the profile tutorial
# def profile(fnc):
#     def inner(*args, **kwargs):
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = fnc(*args, **kwargs)
#         pr.disable()
#         s = io.StringIO()
#         sortby = SortKey.TIME
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         # print(s.getvalue())
#         with open('test.txt', 'w+') as f:
#             f.write(s.getvalue())
#
#         return retval
#     return inner


# Pro github URL soll nun eine Zeile erstellt werden
def one_row_each_URL(df):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    new_header = list(df)
    new_header.insert(0, "None")
    csv_writer.writerow(new_header)

    indexInt = 0

    for row in df.itertuples():
        if row.no_of_github_URLs > 0:
            github_url_converted = literal_eval(row.github_url)
            for url in github_url_converted:
                github_user_profile = add_profile_link(url)
                row_data = [indexInt, row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice, row.description,
                            url, 1, row.other_urls, row.no_of_other_URLs, github_user_profile, None]
                csv_writer.writerow(row_data)
                indexInt += 1
                # new_df.loc[len(new_df)] = row_data
        else:  # leave row untouched if no github URL available
            row_data = [indexInt, row.notice_id, row.file_link, row.year, row.month, row.day, row.header, row.notice, row.description,
                        row.github_url, row.no_of_github_URLs, row.other_urls, row.no_of_other_URLs, row.github_user, None]
            csv_writer.writerow(row_data)
            indexInt += 1
    # new_df_csv.seek(0)
    return new_df_csv


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


def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()

    df_data = pd.read_csv("output_final.csv", keep_default_na=False)

    # Add columns:
    df_data["http_status"] = ""


    with open("output_2_final.csv", mode="w") as output_file:
        new_df = one_row_each_URL(df_data)
        output_file.write(new_df.getvalue())
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
