import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import scipy.stats as stats
import math
import plotly.express as px
import random

from ast import literal_eval  # datatype list get converted to string in .csv files

import time  # measure total run time of program
import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry

SIXTY_MINUTES = 3600


@sleep_and_retry
@limits(calls=5000, period=SIXTY_MINUTES)
def get_GHuser_profile_data(input_data):
    no_of_added_profile_data = 0

    for row in input_data.itertuples():
        index = getattr(row, "Index")

        # TODO: testing
        # if no_of_added_profile_data == 10:
        #     break

        print("Index: ", index)

        # Each 100 added URLs: save backup to file
        if no_of_added_profile_data % 30 == 0 and no_of_added_profile_data != 0:
            print("Saving backup file (current index: ", index)
            write_to_csv_file(input_data)
            print("Saved backup file")

        if len(row.login) == 0 and len(str(row.id)) > 0:
            api_url = "https://api.github.com/user/" + str(row.id)
            try:
                gh_profile_data = requests.get(api_url, auth=("phzeller", "f16eface45cf06c457831303f84433efd5f3bcce"))
            except:
                print(Exception)
                print("Problem found with ID: ", str(row.id))
                write_to_csv_file(input_data)
            else:
                if gh_profile_data.status_code == 200:
                    print(gh_profile_data.status_code)
                    input_data["github_user"].at[index] = gh_profile_data.json()["html_url"]
                    input_data["login"].at[index] = gh_profile_data.json()["login"]
                    input_data["type"].at[index] = gh_profile_data.json()["type"]
                    input_data["company"].at[index] = gh_profile_data.json()["company"]
                    input_data["blog"].at[index] = gh_profile_data.json()["blog"]
                    input_data["location"].at[index] = gh_profile_data.json()["location"]
                    input_data["email"].at[index] = gh_profile_data.json()["email"]
                    input_data["hireable"].at[index] = gh_profile_data.json()["hireable"]
                    input_data["public_repos"].at[index] = gh_profile_data.json()["public_repos"]
                    input_data["public_gists"].at[index] = gh_profile_data.json()["public_gists"]
                    input_data["followers"].at[index] = gh_profile_data.json()["followers"]
                    input_data["following"].at[index] = gh_profile_data.json()["following"]
                    input_data["created_at"].at[index] = gh_profile_data.json()["created_at"]
                    input_data["updated_at"].at[index] = gh_profile_data.json()["updated_at"]
                    input_data["id"].at[index] = gh_profile_data.json()["id"]

                    creation_date = gh_profile_data.json()["created_at"].split("-")

                    new_creation_date = []
                    if len(creation_date) > 0:
                        for elem in creation_date:
                            new_creation_date.append(elem.split("T")[0])
                    if len(new_creation_date) == 3:
                        input_data["creation_year"].at[index] = new_creation_date[0]
                        input_data["creation_month"].at[index] = new_creation_date[1]
                        input_data["creation_day"].at[index] = new_creation_date[2]

                elif gh_profile_data.status_code == 403:
                    raise Exception('API response: {}'.format(gh_profile_data.status_code))
                else:
                    print("ERROR for ID: ", str(row.id))
                    input_data["login"].at[index] = "error"

            finally:
                no_of_added_profile_data += 1


    print("Added this amount:", no_of_added_profile_data)
    return input_data

    # return input_data


def write_to_csv_file(input_data):
    input_data.to_csv("randomized_sample_data.csv")


def main():
    print("Starting request_random_sample_user_data.py:")
    start_time = time.time()

    sample = pd.read_csv("randomized_sample_data.csv", sep=",", keep_default_na=False, index_col=0)

    requested_data = get_GHuser_profile_data(sample)

    write_to_csv_file(requested_data)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
