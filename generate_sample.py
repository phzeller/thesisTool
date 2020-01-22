import time  # measure total run time of program
import pandas as pd
import requests

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import scipy.stats as stats
import math
import plotly.express as px
import random

from csv import writer
from io import StringIO



def generate_sample_IDs(input):
    new_df_csv = StringIO()
    csv_writer = writer(new_df_csv)
    # write header to csv file in memory
    new_header = list(input)
    csv_writer.writerow(new_header)

    for row in input.itertuples():
        index = getattr(row, "Index")

        # TODO: testing
        # if index == 20:
        #     break

        # take existing user id and shift it with randomized values from 1 to 20
        if len(row.id) > 0:
            new_id = int(row.id) + np.random.randint(1, 10)
            csv_writer.writerow([new_id])

    return new_df_csv

def main():
    print("Starting generate_sample.py:")
    start_time = time.time()

    dmca_dataset = pd.read_csv("profile_data_unique_no_dup_with_index_and_year.csv", sep=",", keep_default_na=False,
                               usecols=["id"])



    with open("randomized_sample.csv", mode="w") as output_file:
        new_sample = generate_sample_IDs(dmca_dataset)
        output_file.write(new_sample.getvalue())

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()