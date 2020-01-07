import pandas as pd
import time  # measure total run time of program
from ast import literal_eval # datatype list get converted to string in .csv files



#Pro github URL soll nun eine Zeile erstellt werden
def one_row_each_URL(df):
    testInt = 0
    new_df = pd.DataFrame(columns=list(df))
    for row in df.itertuples():

        # TODO TEST delete testInt and if condition
        testInt += 1
        print(testInt)
        if testInt == 100: return new_df

        if isinstance(row.github_url, str): # NaN entries are treated as float, those should not be investigated
            github_url_converted = literal_eval(row.github_url)
            for url in github_url_converted:
                row_data = [row.notice_id, row.year, row.month, row.day, row.header, row.notice, row.copyright_holder,
                            url, 1, row.other_urls, row.no_of_other_URLs, row.github_user]
                new_df.loc[len(new_df)] = row_data
        else: # remain row untouched if no github URL available
            row_data = [row.notice_id, row.year, row.month, row.day, row.header, row.notice, row.copyright_holder,
                        row.github_url, row.no_of_github_URLs, row.other_urls, row.no_of_other_URLs, row.github_user]
            new_df.loc[len(new_df)] = row_data

    return new_df

def add_profile_link(df):
    df

    return df

def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()

    df_data = pd.read_csv("output.csv")
    new_df = one_row_each_URL(df_data)
    new_df = add_profile_link(new_df)
    new_df.to_csv("output_2_test.csv")
    print("time elapsed: {:.2f}s".format(time.time() - start_time))

if __name__ == '__main__':
    main()