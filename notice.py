import numpy as np
import mistune
from bs4 import BeautifulSoup

import analyzeData
from main import profile



class DMCA_notice:
    @profile
    def __init__(self, info_arr):
        if (isinstance(info_arr, np.ndarray)) and info_arr.size == 2:
            self.filePath = info_arr[0]
            self.file_link = "file://" + self.filePath
            self.title = info_arr[1]

            # TODO: test without beautifulsoup
            self.content = BeautifulSoup(self.markdownToHTML(), "lxml")

            # Merge all relevant data into one list
            self.mined_list = None

            # All relevant data that has to be mined
            self.year = None
            self.month = None
            self.day = None
            self.header = None
            self.notice = "undetermined"
            self.description = ""
            self.github_url = None
            self.github_url_count = 0
            self.other_url = None
            self.other_url_count = 0
            self.github_repo = None
            self.github_user = None
            self.copyright_owner = None


    # TODO for testing:
    def testing(self):
        print("Einen Treffer gefunden:", self.title, "--> Programm wird beendet")
        print(self.github_url)
        print(self.content.prettify())

    def markdownToHTML(self):
        with open(self.filePath) as file:
            return mistune.markdown(file.read().lower())
            return file.read()

    @profile
    def mineData(self):
        # Mining data for required information as mentioned above
        analyzeData.analyzeTitle(self)  # This function determines year, month, day and header
        analyzeData.checkTypeOfNotice(self)   # determines if it's notice, counter-notice, retraction or reversal
        analyzeData.getURLs(self)   # this function determines github_url and copyright_url
        # analyzeData.getKeywords(self)
        if self.github_url is not None:
            self.github_url_count = len(self.github_url)
        if self.other_url is not None:
            self.other_url_count = len(self.other_url)


    def create_list_for_mined_data(self):
        # Merge all relevant data into one list
        self.mined_list = [self.file_link, self.year, self.month, self.day, self.header, self.notice, self.description, self.github_url, self.github_url_count, self.other_url, self.other_url_count, self.github_user]
