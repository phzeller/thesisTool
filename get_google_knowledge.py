from __future__ import print_function
import json
import urllib
import re
import time  # measure total run time of program
import pandas as pd
import requests


def get_google_knowledge_results(input):
    no_of_added_activities = 0

    for row in input.itertuples():
        checkInt = 0
        index = getattr(row, 'Index')

        if index % 25 == 0 and index != 0:
            print("Current process: ", index)

        # Each 20 added URLs: save backup to file
        if no_of_added_activities % 100 == 0 and no_of_added_activities != 0:
            print("Saving backup file")
            write_to_csv_file(input)
            print("Saved backup file")

        # # TODO: TESTING
        # if no_of_added_activities == 10:
        #     print("Test: No. of checked rows in total: ", index, "while added this amout of rows: ",
        #           no_of_added_activities)
        #     return input

        if len(row.google_name) == 0 and row.notice == "notice":
            # grab description of notice and delete any notice_numbers within description (eg. adobe-1, adobe-2, ...)
            regex = r"-[\d]+$"
            fixed_description = re.sub(regex, "", row.description)

            # make google knowledge graph API request

            api_key = "AIzaSyB-X6XKLgoL7Spa1ojLBcJYa52YjRGIN8U"
            query = fixed_description
            service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
            params = {
                'query': query,
                'limit': 1,
                'indent': True,
                'key': api_key,
            }
            url = service_url + '?' + urllib.parse.urlencode(params)
            response = json.loads(urllib.request.urlopen(url).read())

            if "itemListElement" in response:
                for element in response['itemListElement']:
                    if "result" in element:
                        if "name" in element["result"]:
                            input["google_name"].at[index] = element["result"]["name"]
                            checkInt = 1
                        if "@type" in element["result"]:
                            input["google_type"].at[index] = element["result"]["@type"]
                            checkInt = 1
                        if "description" in element["result"]:
                            input["google_description"].at[index] = element["result"]["description"]
                            checkInt = 1
                        if "url" in element["result"]:
                            input["google_url"].at[index] = element["result"]["url"]
                            checkInt = 1
                    if "resultScore" in element:
                        input["google_resultScore"].at[index] = element["resultScore"]
                        checkInt = 1

        if checkInt == 0:
            input["google_name"].at[index] = "not found"
        else:
            no_of_added_activities += 1

    return input


def write_to_csv_file(input_data):
    input_data.to_csv("dmca_notices_with_google_knowledge.csv")


def main():
    print("Starting dmca_notices_with_google_knowledge.py:")
    start_time = time.time()

    csv_input = pd.read_csv("dmca_notices_with_google_knowledge.csv", sep=",", keep_default_na=False, index_col=0)

    new_file = get_google_knowledge_results(csv_input)

    write_to_csv_file(new_file)

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()
