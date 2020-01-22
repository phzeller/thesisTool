import pandas as pd
import re  # use regex to make sure that certain format guidelines are followed
import time  # measure total run time of program
from ast import literal_eval  # datatype list get converted to string in .csv files

from csv import writer
from io import StringIO

def get_index_and_year(input):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    new_header = list(input)
    for add_column in ["id", "creation_year", "creation_month", "creation_day"]:
        new_header.append(add_column)
    csv_writer.writerow(new_header)

    for row in input.itertuples():
        index = getattr(row, "Index")
        # TODO: testing
        # if index == 200:
        #     break
        # ensure, that profile_data contains valid profile_data
        if len(row.profile_data) > 200:
            profile_data_dict = literal_eval(row.profile_data)
            creation_date = row.created_at.split("-")

            new_creation_date = []
            if len(creation_date) > 0:
                for elem in creation_date:
                    new_creation_date.append(elem.split("T")[0])

            else:
                print("Found problem with github_user: ", row.github_user)

            # add index, creation_year, creation_month and creation_day to csv_file
            if len(new_creation_date) > 0:
                row_data = [row.github_user, row.profile_data, row.login, row.type, row.company, row.blog,
                                    row.location, row.email, row.hireable, row.public_repos, row.public_gists,
                                    row.followers, row.following, row.created_at, row.updated_at, profile_data_dict["id"]]
                for date_elem in new_creation_date:
                    row_data.append(date_elem)
                csv_writer.writerow(row_data)
        else:
            print("Problem found with github user: ", row.github_user, "(no valid profile data found)")
            row_data = [row.github_user, row.profile_data, row.login, row.type, row.company, row.blog,
                        row.location, row.email, row.hireable, row.public_repos, row.public_gists,
                        row.followers, row.following, row.created_at, row.updated_at, None, None, None, None]
            csv_writer.writerow(row_data)






    return new_df_csv

def main():
    print("get_index_for_users.py:")
    start_time = time.time()

    csv_input = pd.read_csv("profile_data_unique_no_dup.csv", sep=",", keep_default_na=False, index_col=0)


    with open("profile_data_unique_no_dup_with_index_and_year.csv", mode="w") as output_file:
        new_df = get_index_and_year(csv_input)

        output_file.write(new_df.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()