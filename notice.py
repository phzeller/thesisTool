import numpy as np
import mistune
import pandas as pd
#TODO TESTING import
import sys
from bs4 import BeautifulSoup

import analyzeData


class DMCA_notice:
    def __init__(self, info_arr):
        if (isinstance(info_arr, np.ndarray)) and info_arr.size == 2:
            self.filePath = info_arr[0]
            self.title = info_arr[1]
            self.content = BeautifulSoup(self.markdownToHTML(), "lxml")
            # Merge all relevant data into one dataframe
            self.mined_list = None

            # All relevant data that has to be mined
            self.year = None
            self.month = None
            self.day = None
            self.header = None
            self.notice = None  # is notice counter notice or notice? True if notice, False if counter-notice
            self.copyright_holder = None
            self.github_url = None
            self.copyright_url = None
            self.github_user = None

    # TODO for testing:
    def testing(self):
        print("Einen Treffer gefunden:", self.title, "--> Programm wird beendet")
        print(self.content.prettify())
        sys.exit(0)

    def markdownToHTML(self):
        with open(self.filePath) as file:
            html_file = mistune.markdown(file.read())
            return html_file


    def mineData(self):
        # Mining data for required information as mentioned above
        analyzeData.analyzeTitle(self)  # This function determines year, month, day and header
        analyzeData.checkTypeOfNotice(self)   # true if notice, false if counternotice
        analyzeData.getURLs(self)   # this function determines github_url and copyright_url



    def create_DF_for_mined_data(self):
        # Merge all relevant data into one dataframe
        self.mined_list = [self.year, self.month, self.day, self.header, self.notice, self.copyright_holder, self.github_url, self.copyright_url, self.github_user]
