import time  # measure total run time of program
import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry

SIXTY_MINUTES = 3600


@sleep_and_retry
@limits(calls=4999, period=SIXTY_MINUTES)
def get_GHuser_profile_data(input_data):
    no_of_checked_rows = 0
    no_of_added_profile_data = 0

    for row in input_data.itertuples():
        if no_of_checked_rows % 100 == 0 and no_of_checked_rows != 0:
            print("Current process: ", no_of_checked_rows)

        # Each 100 added URLs: save backup to file
        # if no_of_added_profile_data % 100 == 0 and no_of_added_profile_data != 0:
        #     print("Saving backup file")
        #     write_to_csv_file(input_data)
        #     print("Saved backup file")

        # TODO: TESTING
        # if no_of_added_profile_data == 150:
        #     print("Test: No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
        #           no_of_added_profile_data)
        #     return input_data

        if len(row.profile_data) == 0 and len(row.github_user) > 0:
            try:
                api_url = "https://api.github.com/users/" + row.github_user.split(".com")[1].replace("/", "")
                gh_profile_data = requests.get(api_url, auth=("phzeller", "f16eface45cf06c457831303f84433efd5f3bcce"))
            except Exception:
                print(Exception)
                print("Problem found with User: ", row.github_user)
                input_data["profile_data"].at[no_of_checked_rows] = "error"
            else:
                if gh_profile_data.status_code == 200:
                    print(gh_profile_data.status_code)
                    input_data["profile_data"].at[no_of_checked_rows] = gh_profile_data.json()
                    input_data["login"].at[no_of_checked_rows] = gh_profile_data.json()["login"]
                    input_data["type"].at[no_of_checked_rows] = gh_profile_data.json()["type"]
                    input_data["company"].at[no_of_checked_rows] = gh_profile_data.json()["company"]
                    input_data["blog"].at[no_of_checked_rows] = gh_profile_data.json()["blog"]
                    input_data["location"].at[no_of_checked_rows] = gh_profile_data.json()["location"]
                    input_data["email"].at[no_of_checked_rows] = gh_profile_data.json()["email"]
                    input_data["hireable"].at[no_of_checked_rows] = gh_profile_data.json()["hireable"]
                    input_data["public_repos"].at[no_of_checked_rows] = gh_profile_data.json()["public_repos"]
                    input_data["public_gists"].at[no_of_checked_rows] = gh_profile_data.json()["public_gists"]
                    input_data["followers"].at[no_of_checked_rows] = gh_profile_data.json()["followers"]
                    input_data["following"].at[no_of_checked_rows] = gh_profile_data.json()["following"]
                    input_data["created_at"].at[no_of_checked_rows] = gh_profile_data.json()["created_at"]
                    input_data["updated_at"].at[no_of_checked_rows] = gh_profile_data.json()["updated_at"]
                elif gh_profile_data.status_code == 403:
                    raise Exception('API response: {}'.format(gh_profile_data.status_code))
                else:
                    print("ERROR for user: ", row.github_user)
                    input_data["profile_data"].at[no_of_checked_rows] = "error: status_code " + str(
                        gh_profile_data.status_code)

            finally:
                no_of_added_profile_data += 1

        no_of_checked_rows += 1

    print("No. of checked rows in total: ", no_of_checked_rows, "while added this amout of rows: ",
          no_of_added_profile_data)
    return input_data


def write_to_csv_file(input_data):
    input_data.to_csv("new_profile_data_file.csv")


def main():
    print("Starting dataFrameActions.py:")
    start_time = time.time()

    csv_input = pd.read_csv("new_profile_data_file.csv", sep=",", keep_default_na=False,
                            usecols=["github_user", "profile_data", "login", "type", "company", "blog", "location",
                                     "email", "hireable", "public_repos", "public_gists", "followers", "following",
                                     "created_at", "updated_at"])

    new_file = get_GHuser_profile_data(csv_input)

    write_to_csv_file(new_file)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
