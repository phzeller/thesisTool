import pandas as pd
import re  # use regex to make sure that certain format guidelines are followed
import time  # measure total run time of program
from ast import literal_eval  # datatype list get converted to string in .csv files

from csv import writer
from io import StringIO

# Pro activity soll nun eine Zeile erstellt werden
def one_row_each_URL(input_data):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    new_header = [None, "login", "created_at", "activity_year", "activity_month", "activity_day", "activity_count"]

    csv_writer.writerow(new_header)

    for row in input_data.itertuples():
        index = getattr(row, "Index")
        if index%100 == 0 and index != 0:
            print("Current index: ", index)

        # TODO: testing
        # if index == 50:
        #     break

        if len(row.activity_data) > 0:
            activity_data_list = literal_eval(row.activity_data)
            # Check if there is any activity list in this row
            if len(activity_data_list) > 0:
                for elem in activity_data_list:
                    # Check which years contain activity events
                    if len(elem) > 0:
                        # loop through year list and generate one row per activity_event
                        for activity_entry in elem:
                            # Check if activity_date is formatted correct:
                            if len(activity_entry) == 2:
                                # Split each event date
                                activity_date = activity_entry[0]
                                event_date = activity_date.split("-")
                                # Check if event_date is formatted correct
                                if len(event_date) == 3:
                                    row_data = [index, row.login, row.created_at, int(event_date[0]), int(event_date[1]), int(event_date[2]), int(activity_entry[1])]
                                    csv_writer.writerow(row_data)

    return new_df_csv

def main():
    print("Starting expand_activity.py:")
    start_time = time.time()

    csv_input = pd.read_csv("/Users/philippzeller/Dropbox/Eigener Studienordner/Studium/7. Semester/BA/Backups Python/20_activity_data_v2.csv", sep=",", keep_default_na=False,
                            usecols=["login", "created_at", "activity_data"])


    with open("21_activity_data_rows_v2.csv", mode="w") as output_file:
        new_df = one_row_each_URL(csv_input)
        output_file.write(new_df.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()