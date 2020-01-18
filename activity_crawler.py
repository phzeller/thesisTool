import time  # measure total run time of program
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_activity_data(input):
    no_of_checked_rows = 0
    no_of_added_activities = 0


    for row in input.itertuples():
        print(no_of_checked_rows)
        if no_of_checked_rows % 100 == 0 and no_of_checked_rows != 0:
            print("Current process: ", no_of_checked_rows)

        # Each 20 added URLs: save backup to file
        if no_of_added_activities % 20 == 0 and no_of_added_activities != 0:
            print("Saving backup file")
            write_to_csv_file(input)
            print("Saved backup file")

        # TODO: TESTING
        # if no_of_added_activities == 2:
        #     print("Test: No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
        #           no_of_added_activities)
        #     return input

        if len(row.activity_data) == 0 and len(row.login) > 0:
            activity_list = []
            split_creation_date = row.created_at.split("-")
            # if no correct date format, leave row untouched
            if len(split_creation_date) < 2:
                no_of_checked_rows += 1
                continue
            else:
                account_creation_year = int(row.created_at.split("-")[0])
                years_to_be_checked = determine_years(account_creation_year)
                if 0 < len(years_to_be_checked) < 8:
                    successfulInt = 1
                    for year in years_to_be_checked:
                        year_data = []
                        request_url = "https://github.com/users/" + row.login + "/contributions?to=" + str(year) + "-12-31"
                        try:
                            data_page = requests.get(request_url)
                        except:
                            print(Exception)
                            print("Problem found with User: ", row.login)
                            successfulInt = 0
                            year_data = []
                            break
                        else:
                            soup = BeautifulSoup(data_page.content, "lxml")
                            activity_data_list = soup.find_all("rect")
                            for date in activity_data_list:
                                day = [date.get("data-date"), date.get("data-count")]
                                year_data.append(day)
                            activity_list.append(year_data)

                    if successfulInt == 0:
                        print("keine Daten für login eingetragen: ", row.login)
                        continue
                    else:
                        input["activity_data"].at[no_of_checked_rows] = activity_list
                        no_of_added_activities += 1

                else: print("Found problem in years_to_be_checked with login: ", row.login, "len: ",len(years_to_be_checked))

        no_of_checked_rows += 1

    print("No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
          no_of_added_activities)
    return input




def determine_years(creation_year):
    years = []
    if creation_year < 2013:
        creation_year = 2013
    for year in range(creation_year, 2020):
        years.append(year)
    return years

def write_to_csv_file(input_data):
    input_data.to_csv("activity_data.csv")


def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()

    csv_input = pd.read_csv("activity_data.csv", sep=",", keep_default_na=False, index_col=0)

    scrape_activity_data(csv_input)

    write_to_csv_file(csv_input)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()